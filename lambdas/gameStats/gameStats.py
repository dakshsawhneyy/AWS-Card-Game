import boto3
import json
import traceback

dynamodb = boto3.resource('dynamodb')
game_table = dynamodb.Table('GameSession')
players_table = dynamodb.Table('Players')

def lambda_handler(event, context):
    try:
        game_id = event['queryStringParameters']['GameID']  # Get doesnt support body, so it needs to recieve data in params
        
        game_session = game_table.get_item(Key = {'GameID':game_id}).get('Item')
        if not game_session:
            return {'statusCode': 404, 'body': json.dumps({'message': 'Game not found'}), 'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
        
        # import player_ids
        player_ids = game_session['Players']
        
        # Storing Players info
        players_info = []   # A dictionary
        for pid in player_ids:
            player = players_table.get_item(Key = {'PlayerID':pid}).get('Item')
            # if player is not empty, them append to players
            if player:
                players_info.append({   # Appending into dictionary
                    'Name': player['PlayerName'],
                    'PlayerID': pid,
                    'Health': int(player['Health']),
                    'HandSize': int(len(player.get('Hand',[]))),
                    'Shield': player.get('Shield', None),
                    'Hand': player.get('Hand',[]),
                    'Status': player.get('Status','Active')
                })
                
        # Show Deck Size
        deck = game_session.get('Deck',[])
        deckLength = len(deck)
        
        # Show Current Player Turn
        current_turn = game_session.get('CurrentTurn', None)
                
        return { 
            'statusCode': 200, 
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'  # optional, keep if you might use cookies or auth
            },
            'body': json.dumps({ 'Game': game_session, 'Players': players_info, 'DeckLength': deckLength, 'CurrentTurn': current_turn }) 
        }
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()   # print detailed info about what went wrong.
        return { 
            'statusCode': 500, 
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'  # optional, keep if you might use cookies or auth
            },
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)}) 
        }