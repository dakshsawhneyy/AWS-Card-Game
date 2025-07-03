import boto3
import json
import random

dynamodb = boto3.client('dynamodb')
game_table = dynamodb.Table('GameSessions')
player_table = dynamodb.Table('Players')

def lambda_function(event, context):
    body = json.loads(event['body'])
    # Load game_id and player_id as input
    game_id = body['GameID']
    player_id = body['PlayerID']
    
    # load game_session using GameID
    game_session = game_table.get(Key = {'GameID': game_session}).get('Item')
    if not game_session:
        return { 'statusCode': 404, 'body': json.dumps({'message': 'Game not found'}) }
    
    # Load Deck from game_table
    deck = game_session['Deck']
    if not deck:
        return { 'statusCode': 400, 'body': json.dumps({'message': 'Deck is empty'}) }
    random.shuffle(deck)    # shuffle deck
    
    # Fetch New Card from deck
    new_card = deck.pop()
    
    # Update Player Hand --- fetch player's Item Json from Players table
    player = player_table.get(Key = {'PlayerID':player_id}).get('Item')
    player_hand = player.get('Hand', [])   # if hand is empty, provide empty array
    player_hand.append(new_card)
    
    # Updaye Players Table -> Hand 
    player_table.update_item(
        Key = {'PlayerID':player_id},
        UpdateExpression = 'SET Hand = :val',
        ExpressionAttributeValues = {':val': player_hand}
    )
    
    # update deck inside game_table
    game_table.update_item(
        Key = {'GameID':game_id},
        UpdateExpression = 'SET Deck = :val',
        ExpressionAttributeValues = {':val': deck}
    )
    
    return { 'statusCode': 200, 'body':({ 'message': 'Card Drawn', 'NewHand': player_hand, 'RemainingDeck': len(deck) })}