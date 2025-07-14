import boto3
import json
import traceback

dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table('GameSession')
player_table = dynamodb.Table('Players')

cloudwatch = boto3.client('cloudwatch')     # pushing metrics like attack cards thrown, special and heal to cloudwatch

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        game_id = body['GameID']
        player_id = body['PlayerID']
        winner_id = body.get('WinnerID')    # if no gameID found, no issues return None
        
        # we need to conditionally update game_data because even if winnerID doesnt exist, we need to update Status - ended otherwise validationError
                
        # Updating Status
        update_exp = 'SET #s = :s'
        exp_attr_names = {'#s': 'Status'}
        exp_attr_values = {':s': 'ended'}
        
            
        game_session = game_table.get_item(Key = {'GameID': game_id}).get('Item')
        player_ids = game_session['Players']
            
        # only admin can manually end the game, no other player can
        if player_id != player_ids[0]:
            return { 'statusCode': 403, 'body': json.dumps({'message': 'Forbidden: Only the game admin can end the game.'}),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}

        # Manually end the game if only one active player is left
        active_players = []
        for pid in player_ids:
            player_info = player_table.get_item(Key={'PlayerID': pid}).get('Item')
            if player_info and player_info.get('Status') == 'Active':
                active_players.append(pid)                

        # If 1 active player lefts, declare him as winner
        if len(active_players) == 1:
            winner_id = active_players[0]
            
            
        # if WinnerID exists, then add updated winner expressison into update_exp variable
        if winner_id:
            update_exp += ', #w = :w'
            exp_attr_names['#w'] = 'WinnerID'
            exp_attr_values[':w'] = winner_id
            
            
        # Update game_table
        game_table.update_item(
            Key = {'GameID':game_id},
            UpdateExpression = update_exp,
            ExpressionAttributeNames = exp_attr_names,
            ExpressionAttributeValues = exp_attr_values   
        )
        
        # adding metrics to cloud watch -- per player so that we get metrics per player
        for pid in player_ids:
            p_info = player_table.get_item(Key={'PlayerID':pid}).get('Item', {})
            cloudwatch.put_metric_data(     # fetch metrics per player -- without this we combine all player usage
                Namespace = 'CardGameMetrics',
                MetricData = [
                    {
                        'MetricName': 'AttackCardsThrown',
                        'Dimensions': [{'Name': 'PlayerID', 'Value': p_info['PlayerName']}],
                        'Value': p_info.get('TotalAttacks', 0),
                        'Unit': 'Count'
                    },
                    {
                        'MetricName': 'DamageDealt',
                        'Dimensions': [{'Name': 'PlayerID', 'Value': p_info['PlayerName']}],
                        'Value': p_info.get('TotalDamageDealt', 0),
                        'Unit': 'Count'
                    },
                    {
                        'MetricName': 'SpecialCardsThrown',
                        'Dimensions': [{'Name': 'PlayerID', 'Value': p_info['PlayerName']}],
                        'Value': p_info.get('TotalSpecial', 0),
                        'Unit': 'Count'
                    },
                    {
                        'MetricName': 'HealCardsThrown',
                        'Dimensions': [{'Name': 'PlayerID', 'Value': p_info['PlayerName']}],
                        'Value': p_info.get('TotalHeals', 0),
                        'Unit': 'Count'
                    }
                ]
            )
        
        return { 'statusCode': 200, 'body': json.dumps({ 'message':'Game Ended', 'Winner': winner_id if winner_id else None }),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'} }
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()   # print detailed info about what went wrong.
        return { 'statusCode': 500, 'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)}),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'} }