import boto3
import json
import traceback
import random

dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table('GameSession')
player_table = dynamodb.Table('Players')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])     # Fetch GameID, PlayerID and CardID player has dropped
        game_id = body['GameID']        
        player_id = body['PlayerID']
        card_id = body['CardID']
        
        # import game_session
        game_session = game_table.get_item(Key = {'GameID':game_id}).get('Item')
        if not game_session:
            return {'statusCode': 404, 'body': json.dumps({'message': 'Game not found'}),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
        
        # Check if its current player's turn, if yes then only proceed 
        if player_id != game_session['CurrentTurn']:
            return { 'statusCode': 400, 'body': json.dumps({ 'message': 'Not your turn' }), 'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
        
        # import player and his hand
        player = player_table.get_item(Key = {'PlayerID':player_id}).get('Item')
        hand = player['Hand']
        
        # Fetch that card using CardID from player's hand
        card = next((c for c in hand if c['CardID'] == card_id), None)  # if not found, return None without giving error
        
        #! Loop inside hand and remove that card with CardID == card_id - hand has two items: {CardType,CardID}
        updated_hand = [c for c in hand if c['CardID'] != card_id]   #! gimme list as o/p and loop on every card & check if c is not card we want to throw, add to updated hand
        # check if length of hand == updated_hand, meaning no card is thrown
        if len(hand) == len(updated_hand):
            return {'statusCode': 400, 'body': json.dumps({'message': 'Card not found in hand'}), 'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
        
        # Determine Next Player Turn - by fetching player_ids from game_table and add 1 to its id
        player_ids = game_session.get('Players', [])
        
        curr_index = player_ids.index(player_id)
        
        # Adding logic to skip turn of player, if he's eliminated
        while True:
            next_index = (curr_index + 1) % len(player_ids)    # fetch index of curr player from up list and add 1 to it
            next_player_id = player_ids[next_index]
            
            next_player_info = player_table.get_item(Key = {'PlayerID':next_player_id}).get('Item')
            
            # check elimination status
            if next_player_info['Status'] != 'Eliminated':
                break
            else:
                curr_index = next_index
        
        next_turn = player_ids[next_index]
        
        
        next_turn_player_info = player_table.get_item(Key = {'PlayerID':next_turn}).get('Item')        
        hand_for_special = updated_hand.copy()
        
        #! Apply Affect to player
        if card['Type'] == 'attack':
            if next_turn_player_info.get('Shield',False) == False:
                Health = next_turn_player_info.get('Health', 100)
                Health = Health - 20
                if Health <= 0:
                    next_turn_player_info['Status'] = 'Eliminated' # Eliminate Player from game
                next_turn_player_info['Health'] = Health    # Update Health of player
            else:
                # If it is true, update player table and make it false
                player_table.update_item(
                    Key = {'PlayerID': next_turn},
                    UpdateExpression = 'SET Shield = :s',
                    ExpressionAttributeValues = {':s': False}   # Set shield to False
                )
            
        elif card['Type'] == 'defence':
            # Add shield into player inside player_table
            player_table.update_item(
                Key = {'PlayerID': player_id},
                UpdateExpression = 'SET Shield = :s',
                ExpressionAttributeValues = {':s': True}   # Set shield to True
            )
           
        elif card['Type'] == 'heal':
            Health = player.get('Health', 100)
            if Health + 20 > 100:
                return {'statusCode': 400, 'body': json.dumps({'message': 'Health cannot exceed 100, Throw Another Card'}),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
            else:
                Health = Health + 20
            player['Health'] = Health
        
        elif card['Type'] == 'special':
            # Give a random card to next player
            next_player_hand = next_turn_player_info['Hand']
            if updated_hand:
                random_card = random.choice(updated_hand)
                hand_for_special = [c for c in updated_hand if c['CardID'] != random_card['CardID']]   # store all cards except that stolen one
                next_player_hand.append(random_card)
                player_table.update_item(
                    Key = {'PlayerID':next_turn},
                    UpdateExpression = 'SET Hand = :val',
                    ExpressionAttributeValues = {':val': next_player_hand}   # Update Hand next player
                )
        
        else:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid card type'}),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
        
        updated_hand = hand_for_special
        
        # Update Current Player Table
        player_table.update_item(
            Key = {'PlayerID':player_id},
            UpdateExpression = 'SET Hand = :val, Health = :h',
            ExpressionAttributeValues = {':val': updated_hand, ':h': player['Health']}   # Update Hand and Health of current player
        )
        
        
        # Update Next Player Table
        player_table.update_item(
            Key = {'PlayerID':next_turn},
            UpdateExpression = 'SET Health = :h, #s = :s',
            ExpressionAttributeNames = {'#s': 'Status'},  # Using #s because Status is a reserved keyword in DynamoDB
            ExpressionAttributeValues = {':h': next_turn_player_info['Health'], ':s': next_turn_player_info['Status'] }   # Update Hand and Health of next player
        )
        
        
        # Update Next Turn in GameSessions table
        game_table.update_item(
            Key = {'GameID':game_id},
            UpdateExpression = 'SET CurrentTurn = :val',
            ExpressionAttributeValues = {':val': next_turn}
        )
        
        # Updating winner if after throwing Card, player deck becomes 0, declare him as winner
        WinnerID = None # initially
        active_players = []
        
        for pid in player_ids:
            p_info = player_table.get_item(Key={'PlayerID': pid}).get('Item')
            if p_info and p_info.get('Status') == 'Active':
                active_players.append(pid)
                # if player deck lentgh becomes 0, make him the winner
                if len(p_info.get('Hand',[])) == 0:
                    WinnerID = pid
                    break
                
        # if winner ID nhi hai tb bhi active players 1 hi hai toh usko winner declare krdo
        if not WinnerID and len(active_players) == 1:
            WinnerID = active_players[0]
            
        # Update game table, if WinnerID is present
        if WinnerID:
            game_table.update_item(
                Key = {"GameID":game_id},
                UpdateExpression = 'SET #s = :s, #w = :w',
                ExpressionAttributeNames = { '#s': 'Status', '#w': 'WinnerID' },
                ExpressionAttributeValues = {':s': 'ended', ':w': WinnerID}
            )
        
        return { 'statusCode': 200, 'body': json.dumps({ 'message': 'Card played', 'NextTurn': next_turn}), 'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()   # print detailed info about what went wrong.
        return { 'statusCode': 500, 'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)}), 'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'} }