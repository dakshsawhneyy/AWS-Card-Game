import boto3
import json

dynamodb = boto3.client('dynamodb')
game_table = dynamodb.Table('GameSession')

def lambda_handler(event, context):
    body = json.loads(event[body])
    game_id = body['GameID']
    winner_id = body['WinnerID']
    
    # we need to conditionally update game_data because even if winnerID doesnt exist, we need to update Status - ended otherwise validationError
    
    # Updating Status
    update_exp = 'SET #s = :s'
    exp_attr_names = {'#s': 'Status'}
    exp_attr_values = {':s': 'ended'}
    
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
    
    return { 'statusCode': 200, 'body': json.dumps({ 'message':'Game Ended', 'Winner': winner_id }) }