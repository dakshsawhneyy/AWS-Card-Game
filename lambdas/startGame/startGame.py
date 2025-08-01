import boto3
import json
import random
import traceback

dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table('GameSession')
player_table = dynamodb.Table('Players')

def lambda_handler(event, context):
    try:
        # get GameID as an input
        body = json.loads(event['body'])
        game_id = body['GameID']
        player_id = body['PlayerID']    # only the admin is able to start the game
                
        # fetch game_session from game_table
        game_session = game_table.get_item(Key={'GameID': game_id}).get('Item')
        if not game_session:
            return { 'statusCode': 404, 'body': json.dumps({'message': 'Game not found'}), 'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true' }}
        
        # fetch player_ids from player_table
        player_ids = game_session.get('Players', []) # if no player, then return empty array
        
        # Fetch the id of the player that created the game
        admin_player = player_ids[0]
        
        # if current player is not equal to admin, he cannot start the game
        if player_id != admin_player:
            return { 'statusCode': 403, 'body': json.dumps({'message': 'Only the game creator can start the game'}), 'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
        
        # Atleast 2 players are needed to play the game
        if len(player_ids) < 2:
            return { 'statusCode': 400, 'body': json.dumps({'message': 'At least 2 players are required to start the game'}), 'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true' }}
        
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
        
        return { 
            'statusCode': 200, 
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'  # optional, keep if you might use cookies or auth
            },
            'body': json.dumps({'message': 'Game Started', 'FirstTurn': player_ids[0]}) 
        }
    except Exception as e:
        print(f"Error:", e)
        traceback.print_exc()   # print detailed info about what went wrong.
        return { 
            'statusCode': 500, 
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'  # optional, keep if you might use cookies or auth
            },
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)})
        }