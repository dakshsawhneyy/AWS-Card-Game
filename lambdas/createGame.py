import boto3
import uuid     # Python Library that creates unique id
import random  # Python Library used to take random cards from cards_list
import json     # for using response as json

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GameSession')

# Defining List of Cards
CARD_TYPES = ['attack', 'defence', 'heal', 'special']

# Creating Function for generating_deck
def generate_deck():
    """Create a simple shuffled deck."""    # DocString, tells what a function should do
    deck = []   # initialize deck to empty -- it recieve pair{CardID,card_type}
    
    for _ in range(52):  # '_' means we dont need variable to store count, just create cards and need cards to draw as well
        card_type = random.choice(CARD_TYPES)   # .coice is function inside random - pick random element from list
        card_id = str(uuid.uuid4())
        deck.append({
            'CardID': card_id,
            'Type': card_type
        })
    random.shuffle(deck)    # Shuffle Whole list 
    return deck

def lambda_handler(event, context):
    # Unique GameID using uuid library
    game_id = str(uuid.uuid4())  # uuid4 stands for generate most unique id
    
    # Fetching Creator Name from body
    body = json.loads(event['body'])
    creator_name = body['CreatorName']
    
    # Initialize deck
    deck = generate_deck()
    
    # Create GameSession Entry in DynamoDB
    table.put_item(
        Item={
            'GameID': game_id,
            'Status': 'waiting',
            'Deck': deck,
            'Players': [],
            'CurrentTurn': None,
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
            'CreatorName': creator_name
        })
    }
    
    return response