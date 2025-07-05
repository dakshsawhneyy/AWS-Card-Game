import boto3
import json
import traceback

dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table('GameSession')
players_table = dynamodb.Table('Players')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        game_id = body['GameID']
        
        game_session = game_table.get_item(Key = {'GameID':game_id}).get('Item')
        if not game_session:
            return {'statusCode': 404, 'body': json.dumps({'message': 'Game not found'})}
        
        # import player_ids
        player_ids = game_session['Players']
        
        # Loop over player id, fetch their info and store in players list
        players = []
        for pid in player_ids:
            player = players_table.get_item(Key = {'PlayerID':pid}).get('Item')
            # if player is not empty, them append to players
            if player:
                players.append(player)
                
        return { 'statusCode': 200, 'body': json.dumps({ 'Game': game_session, 'Players': players }) }
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()   # print detailed info about what went wrong.
        return { 'statusCode': 500, 'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)}) }