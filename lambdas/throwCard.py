import boto3
import json

dynamodb = boto3.client('dynamodb')
game_table = dynamodb.Table('GameSession')
player_table = dynamodb.Table('Players')

def lambda_handler(event, context):
    body = json.loads(event['body'])     # Fetch GameID, PlayerID and CardID player has dropped
    game_id = body['GameID']        
    player_id = body['PlayerID']
    card_id = body['CardID']
    
    # import game_session
    game_session = game_table.get(Key = {'GameID':game_id}).get('Item')
    if not game_session:
        return {'statusCode': 404, 'body': json.dumps({'message': 'Game not found'})}
    
    # import player and his hand
    player = player_table.get(Key = {'PlayerID':player_id}).get('Item')
    hand = player['Hand']
    
    #! Loop inside hand and remove that card with CardID == card_id - hand has two items: {CardType,CardID}
    updated_hand = [c for c in hand if c['CardID'] != card_id]   #! gimme list as o/p and loop on every card & check if c is not card we want to throw, add to updated hand
    # check if length of hand == updated_hand, meaning no card is thrown
    if len(hand) == len(updated_hand):
        return {'statusCode': 400, 'body': json.dumps({'message': 'Card not found in hand'})}
    
    # Update Player Table
    player_table.update_item(
        Key = {'PlayerID':player_id},
        UpdateExpression = 'SET Hand = :val',
        ExpressionAttributeValues = {':val': updated_hand}   
    )
    
    # Determine Next Player Turn - by fetching player_ids from game_table and add 1 to its id
    player_ids = game_table.get('Players', [])
    next_index = (player_ids.index(player_id) + 1) % len(player_ids)    # fetch index of curr player from up list and add 1 to it
    next_turn = player_ids[next_index]
    
    # Update Next Turn in GameSessions table
    game_table.update_item(
        Key = {'GameID':game_id},
        UpdateExpression = 'SET CurrentTurn = :val',
        ExpressionAttributeValues = {':val': next_turn}
    )
    
    return { 'statusCode': 200, 'body': ({ 'message': 'Card played', 'NextTurn': next_turn})}