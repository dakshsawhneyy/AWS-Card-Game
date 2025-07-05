import boto3
import json
import random

dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table('GameSession')
player_table = dynamodb.Table('Players')

def lambda_handler(event, context):
    # get GameID as an input
    body = json.loads(event['body'])
    game_id = body['GameID']
    
    # fetch game_session from game_table
    game_session = game_table.get(Key={'GameID': game_id}).get('Item')
    if not game_session:
        return { 'statusCode': 404, 'body': json.dumps({'message': 'Game not found'}) }
    
    # fetch player_ids from player_table
    player_ids = game_session.get('Players', []) # if no player, then return empty array
    
    # Atleast 2 players are needed to play the game
    if len(player_ids) < 2:
        return { 'statusCode': 400, 'body': json.dumps({'message': 'At least 2 players are required to start the game'}) }
    
    # fetch deck and shuffle the deck
    deck = game_session['Deck']
    random.shuffle(deck)  # Shuffle the deck to randomize card distribution
    
    # Give 7 Card to each player - using player_id, go in its player table and update Hand
    for player_id in player_ids:
        hand = []   # initially hand is empty
        for _ in range(7):
            if deck:    # deck doesnt gets empty
                hand.append(deck.pop())   # append card in hand and pop that from deck
        # Update player_table
        player_table.update_item(   
            Key = {'PlayerID': player_id},
            UpdateExpression = 'SET Hand = :val',   # first update the expression
            ExpressionAttributeValues = {':val': hand}  # then insert value
        )
    
    # Update game_session inside game_table
    game_table.update_item(
        Key = {'GameID': game_id},
        UpdateExpression = 'SET #s = :s, Deck = :d, CurrentTurn = :c',  # using #s because Status is a reserved keyword in dynamodb
        ExpressionAttributeNames = { '#s': 'Status' },  # Assigning value to #s
        ExpressionAttributeValues = { ':s': 'ongoing', ':d': deck, ':c': player_ids[0] }
    )
    
    return { 'statusCode': 200, 'body': json.dumps({'message': 'Game Started', 'FirstTurn': player_ids[0]}) }