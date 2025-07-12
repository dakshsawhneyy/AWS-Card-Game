import boto3
import json
import traceback

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Connections')

def lambda_handler(event,context):
    try:
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
                    try:
                        apigw.post_to_connection(
                            ConnectionId=connection_id,
                            Data=json.dumps(game_state).encode('utf-8')
                        )
                    except apigw.exceptions.GoneException:
                        print(f"Stale connection. Deleting {connection_id}")
                        table.delete_item(Key={'ConnectionID': connection_id})
                    except Exception as e:
                        print(f"Error sending to {connection_id}: {str(e)}")
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