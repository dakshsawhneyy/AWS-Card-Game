import boto3
import json

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Connections')

def lambda_handler(event,context):
    # stream has various records, we need its MODIFY record to update modified values 
    for record in event['Records']:     # there can be multiple entries in stream
        if record['eventName'] == 'Modify':     # only if record is modify, then proceed
            # fetch new image that has been modified
            new_image = record['dynamodb']['NewImage']      # NewImage is like a snapshot of latest image
            game_state = json.loads(new_image['GameState']['S'])    #  a column in table that stores entire game state as JSON String
            
            # fetch all connections
            connections = table.scan()['Items'] # read all rows from table, and fetch ConnectionID from each row
            
            # setting up special AWS client to send messages to WebSockets Clients      # endpoint_url is fetched from api gateway made for ws
            apigw = boto3.client('apigatewaymanagementapi', endpoint_url="https://evpfijv179.execute-api.ap-south-1.amazonaws.com/dev-ws")
            
            # send updated state to each player
            for conn in connections:
                connection_id = conn["ConnectionID"]
                apigw.post_to_connection(
                    ConnectionID=connection_id,
                    Data=json.dumps(game_state).encode('utf-8')
                )