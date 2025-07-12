import boto3
import traceback

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Connections')

def lambda_handler(event,context):
    try:
        connectionId = event['requestContext']['connectionId']  # fetch from requestContext and keep connectionId like this, its syntax
        
        print(f"EVENT: {event}")
        print(f"ConnectionID: {connectionId}")
        
        # save connectionId to table i.e. update table
        table.put_item(
            Item = {
                'ConnectionID' : connectionId
            }
        )
        
        print("Successfully wrote to DynamoDB Connections table.")
        
        return {'statusCode': 200}
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