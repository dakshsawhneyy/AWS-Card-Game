import boto3
import traceback

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Connections')

def lambda_handler(event,context):
    try:
        connectionId = event['requestContext']['connectionId']
        
        table.delete_item(
            Key={
                'ConnectionID': connectionId
            }
        )
        
        return {'statusCode': 200}
    except Exception as e:
        print(f"Error disconnecting: {e}")
        traceback.print_exc()  # Print detailed error information
        return {
            'statusCode': 500,
            'body': 'Error disconnecting'
        }