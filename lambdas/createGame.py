import boto3
import uuid     # Python Library that creates unique id
import random  # Python Library used to take random cards from cards_list
import json     # for using response as json
import datetime

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GameSession')
players_table = dynamodb.Table('Players')

# Defining List of Cards
CARD_TYPES = ['attack', 'defence', 'heal', 'special']

# Creating Function for generating_deck
def generate_deck():
    """Create a simple shuffled deck."""    # DocString, tells what a function should do
    deck = []   # initialize deck to empty -- it recieve pair{CardID,card_type}
    
    for _ in range(200):  # '_' means we dont need variable to store count, just create cards and need cards to draw as well
        card_type = random.choice(CARD_TYPES)   # .coice is function inside random - pick random element from list
        card_id = str(uuid.uuid4())[:8]
        deck.append({
            'CardID': card_id,
            'Type': card_type
        })
    random.shuffle(deck)    # Shuffle Whole list 
    return deck

def lambda_handler(event, context):
    # Unique GameID and player id using uuid library
    game_id = str(uuid.uuid4())[:8]  # uuid4 stands for generate most unique id
    player_id = str(uuid.uuid4())[:8]
    
    # Fetching Creator Name from body
    body = json.loads(event['body'])
    creator_name = body['CreatorName']
    
    # Initialize deck
    deck = generate_deck()
    
    # Create Player entry to Database
    players_table.put_item(
        Item = {
            'PlayerID': player_id,
            'GameID': game_id,
            'PlayerName': creator_name,
            'Hand': [],     # we will modify furthur
            'Health': 100,
            'Status': 'Active',
            'LastActionAt': datetime.datetime.now().isoformat(),  # Store current time in ISO format
        }
    )
    
    # Create GameSession Entry in DynamoDB
    table.put_item(
        Item={
            'GameID': game_id,
            'Status': 'waiting',
            'Deck': deck,
            'Players': [player_id],
            'CurrentTurn': player_id,
            'CreatedAt': context.aws_request_id     # Every time AWS Lambda runs, it assigns a unique request ID.
        }
    )
    
    response = {
        'statusCode': 200,
        # Without these headers, error was coming http://localhost:5173' has been blocked by CORS policy
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true'  # optional, keep if you might use cookies or auth
        },
        'body': json.dumps({
            'message': 'Game Created Successfully',
            'GameID': game_id,
            'PlayerID': player_id,
            'CreatorName': creator_name
        })
    }
    
    return response