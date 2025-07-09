import boto3
import uuid
import json
import datetime
import traceback

dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table('GameSession')     # need to fetch items from GameTable by providing GameID
players_table = dynamodb.Table('Players')

def lambda_handler(event, context):
    try:
        player_id = str(uuid.uuid4())[:8]   # generate a random player id -- unique
        
        # Fetch these details from body i.e. whenever a client sends data (postman or frontend), it sends as json object "Body"
        body = json.loads(event['body'])    # Load Body i.e. Load JSON data
        game_id = body['GameID']    # User Inputs GameID
        player_name = body['PlayerName']    # User Inputs Name
        
        # fetch all items or all game_session using game_id as key and fetching items as its value
        game_session = game_table.get_item(Key={'GameID': game_id}).get('Item') # Game ID has value and Items list, we pass GameID and it gives us list of items
        if not game_session:
            return {'statusCode': 404, 'body': json.dumps({'message': 'Game not found'}),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
        
        # If player size exceeds 4, dont add player
        if len(game_session['Players']) > 4:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Cannot join, maximum players reached'}),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
        
        # If Game Already Starts, then give error
        if game_session['Status'] != 'waiting':
            return {'statusCode': 400, 'body': json.dumps({'message': 'Cannot join, game already started'}),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
        
        # Create Player
        players_table.put_item(
            Item = {
                'PlayerID': player_id,
                'GameID': game_id,
                'PlayerName': player_name,
                'Hand': [],     # we will modify furthur
                'Health': 100,
                'Status': 'Active',
                'LastActionAt': datetime.datetime.now().isoformat(),  # Store current time in ISO format
            }   
        )
        
        # Update GameSession Player List
        players = game_session.get('Players', [])   # if no players, you get an empty list
        players.append(player_id)
        game_table.update_item(     # Update Players inside GameSessions Table
            Key = {'GameID': game_id},
            UpdateExpression = 'SET Players = :val',   # Set players value = :val passed in next expression
            ExpressionAttributeValues = {':val': players}
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'
            },
            'body': json.dumps({'message': 'Player Joined Successfully', 'PlayerID': player_id})
        }
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()   # print detailed info about what went wrong.
        return { 
            'statusCode': 500, 
            'headers':{     # Required for error http://localhost:5173' has been blocked by CORS policy
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'
            },
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)}) 
        }