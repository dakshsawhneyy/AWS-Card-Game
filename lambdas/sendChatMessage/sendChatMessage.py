import boto3
import json
import time
import traceback

dynamodb = boto3.resource('dynamodb')
msgTable = dynamodb.Table('gameChatMessages')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        
        game_id = body['GameID']
        sender = body['sender']
        message = body['message']
        
        if not game_id or not sender or not message:
            return {'statusCode': 400, 'body': json.dumps({'message': 'Missing GameID, Sender, or Message'}),'headers': {'Access-Control-Allow-Origin': '*','Access-Control-Allow-Credentials': 'true'}}
        
        time_stamp = int(time.time())  # Get current time
        
        # update table
        msgTable.put_item(
            Item = {
                'GameID': game_id,
                'sender': sender,
                'message': message,
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
    