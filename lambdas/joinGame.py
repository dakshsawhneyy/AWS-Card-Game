import boto3
import uuid
import json
import datetime

dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table('GameSession')     # need to fetch items from GameTable by providing GameID
players_table = dynamodb.Table('Players')

def lambda_handler(event, context):
    player_id = str(uuid.uuid4())   # generate a random player id -- unique
    
    # Fetch these details from body i.e. whenever a client sends data (postman or frontend), it sends as json object "Body"
    body = json.loads(event['body'])    # Load Body i.e. Load JSON data
    game_id = body['GameID']    # User Inputs GameID
    player_name = body['PlayerName']    # User Inputs Name
    
    # fetch all items or all game_session using game_id as key and fetching items as its value
    game_session = game_table.get_item(Key={'GameID': game_id}).get('Item') # Game ID has value and Items list, we pass GameID and it gives us list of items
    if not game_session:
        return {'statusCode': 404, 'body': json.dump({'message': 'Game not found'})}
    
    # If Game Already Starts, then give error
    if game_session['status'] != 'waiting':
        return {'statusCode': 400, 'body': json.dump({'message': 'Cannot join, game already started'})}
    
    # Create Player
    players_table.put_item(
        Item = {
            'PlayerID': player_id,
            'GameID': game_id,
            'PlayerName': player_name,
            'Hand': [],     # we will modify furthur
            'Health': 100,
            'Status': 'Active',
            'LastActionAt': datetime.datetime.now().isoformat,  # Store current time in ISO format
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
        'body': json.dumps({'message': 'Player Joined Successfully', 'PlayerID': player_id})
    }