import boto3
import json
import traceback

dynamodb = boto3.resource('dynamodb')
chat_table = dynamodb.Table('gameChatMessages')

def lambda_handler(event, context):    
    try:
        game_id = event['queryStringParameters']['GameID']   # get request
        
        response = chat_table.query(    # .query is used to retrieve object from DynamoDB Table
            KeyConditionExpression = Key('GameID').eq(game_id),     # fetch all key with game_id
            ScanIndexForward = True,    # ascending order, if false then decending order
            Limit = 20
        )
        
        print(response)
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items']),  # return all items in JSON format -- inside Items our msgs will be present
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'
            }
        }
    
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Credentials': 'true'
            },
            'body': json.dumps({'message': 'Internal Server Error', 'error': str(e)})
        }
    
    