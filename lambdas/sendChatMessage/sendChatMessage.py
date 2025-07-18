import boto3
import json
import time
import traceback

dynamodb = boto3.resource('dynamodb')
msgTable = dynamodb.Table('gameChatMessages')
playerTable = dynamodb.Table('Players')

def lambda_handler(event, context):
    try:
        if 'body' in event:
            body = json.loads(event['body'])  # API Gateway/Lambda call
        else:
            body = event  # Direct Lambda test or internal call
        
        gameID = str(body['GameID'])
        sender = str(body['sender'])
        messg = str(body['messg'])
        
        if not gameID or not sender or not messg:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Missing GameID, Sender, or Message'}),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
        
        time_stamp = str(int(time.time() * 1000))  # Get current time in ms
        
        # Fetching Player Name using sender id
        player_info = playerTable.get_item(Key={'PlayerID': sender}).get('Item')
        player_name = player_info.get('PlayerName', "")
        
        # update table
        msgTable.put_item(
            Item = {
                'GameID': gameID,
                'sender': sender,
                'player_name': player_name,
                'messg': messg,
                'TimeStamp': time_stamp
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Message sent successfully'}),
            'headers': {'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Credentials': 'true'}
        }
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()   # print detailed info about what went wrong.
        return { 
            'statusCode': 500, 
            'headers':{     # Required for error http://localhost:5173' has been blocked by CORS policy
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'
            },
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)}) 
        }
    