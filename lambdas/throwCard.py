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
        
        deck = game_session['Deck']
        
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
        
        # retrieving the values from player_table
        attack_cards = player.get('TotalAttacks', 0)    # even if its not present, initialise it with 0
        damage_dealt = player.get('TotalDamageDealt', 0)
        heal_cards = player.get('TotalHeals', 0)
        special_cards = player.get('TotalSpecial', 0)
        
        #! Apply Affect to player
        if card['Type'] == 'attack':
            attack_cards += 1
            if next_turn_player_info.get('Shield',False) == False:
                damage_dealt += 20      # incrementing damage_dealt
                Health = next_turn_player_info.get('Health', 100)
                Health = Health - 20
                if Health <= 0:
                    next_turn_player_info['Status'] = 'Eliminated' # Eliminate Player from game
                    next_turn_player_info['Health'] = 0 # if its less than 0, make it 0
                else:
                    next_turn_player_info['Health'] = Health    # Update Health of player
                # immediately update next player status
                player_table.update_item(
                    Key = {'PlayerID':next_turn},
                    UpdateExpression = 'SET Health = :h, #s = :s',
                    ExpressionAttributeNames = {'#s': 'Status'},
                    ExpressionAttributeValues = {':h': next_turn_player_info['Health'], ':s': next_turn_player_info['Status'] }   # Update Hand and Health of next player
                )
                # immediately check if only one player remains - declare him as winner # ! Although i was doing same in end, but frontend was seeing still active game status and hence it was not ending
                active_players = []
                for pid in player_ids:
                    p__info = player_table.get_item(Key={'PlayerID':pid}).get('Item')
                    if p__info and p__info['Status'] != 'Eliminated':
                        active_players.append(pid)
                        
                # if length of active players becomes 0, update the winnerID
                if len(active_players) == 1:
                    # update the winner id and table's status and winnerID
                    WinnerID = active_players[0]
                    game_table.update_item(
                        Key = {'GameID': game_id},
                        UpdateExpression = 'SET #s = :s, #w = :w',
                        ExpressionAttributeNames = {'#s': 'Status', '#w': 'WinnerID'},
                        ExpressionAttributeValues = {':s': 'ended', ':w': WinnerID}    
                    )
                    return { 'statusCode': 200, 'body': json.dumps({ 'message': 'Card played. Game Ended', 'WinnerID': WinnerID }), 'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
                    
                
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
            heal_cards += 1     # incrementing heal cards thrown
            Health = player.get('Health', 100)
            Health = min(Health + 20, 100)  # if health goes upto 100, set 100 else min value
            player['Health'] = Health
        
        elif card['Type'] == 'special':
            special_cards += 1      # incrememnt thrown special cards
            # Give a random card to next player
            next_player_hand = next_turn_player_info['Hand']
            if deck:
                num_cards_to_give = min(5,len(deck))
                random_cards = random.sample(deck,num_cards_to_give)     # from deck, pick number of cards to give
                next_player_hand.extend(random_cards)
                deck = [c for c in deck if c not in random_cards]
                player_table.update_item(
                    Key = {'PlayerID':next_turn},
                    UpdateExpression = 'SET Hand = :val',
                    ExpressionAttributeValues = {':val': next_player_hand}   # Update Hand next player
                )
        
        else:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Invalid card type'}),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
                
        # Update Current Player Table
        player_table.update_item(
            Key = {'PlayerID':player_id},
            UpdateExpression = 'SET Hand = :val, Health = :h, TotalSpecial = :s, TotalHeals = :heal, TotalDamageDealt = :dam, TotalAttacks = :attack',
            ExpressionAttributeValues = {':val': updated_hand, ':h': player['Health'], ':s': special_cards, ':heal': heal_cards, ':dam': damage_dealt, ':attack': attack_cards}   # Update Hand and Health of current player
        )
        
        
        # Update Next Turn in GameSessions table
        game_table.update_item(
            Key = {'GameID':game_id},
            UpdateExpression = 'SET CurrentTurn = :val, Deck = :deck',
            ExpressionAttributeValues = {':val': next_turn, ':deck': deck}
        )
        
        # Updating winner if after throwing Card, player deck becomes 0, declare him as winner
        WinnerID = None # initially
        active_players = []
        
        for pid in player_ids:
            p_info = player_table.get_item(Key={'PlayerID': pid}).get('Item')
            if p_info and p_info.get('Status') != 'Eliminated':
                active_players.append(pid)  # not append that player, whose status is eliminated
                #* if player deck length becomes 0, make him the winner
                if not WinnerID and len(p_info.get('Hand',[])) == 0:
                    WinnerID = pid
                    break
                
            
        # Update game table, if WinnerID is present
        if WinnerID:
            game_table.update_item(
                Key = {"GameID":game_id},
                UpdateExpression = 'SET #s = :s, #w = :w',
                ExpressionAttributeNames = { '#s': 'Status', '#w': 'WinnerID' },
                ExpressionAttributeValues = {':s': 'ended', ':w': WinnerID}
            )
        
        return { 'statusCode': 200, 'body': json.dumps({ 'message': 'Card played', 'NextTurn': next_turn, 'WinnerID': WinnerID if WinnerID else None}), 'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
    except Exception as e: 
        print("Error:", e)
        traceback.print_exc()   # print detailed info about what went wrong.
        return { 'statusCode': 500, 'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)}), 'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'} }