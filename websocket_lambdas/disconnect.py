import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Connections')

def lambda_handler(event,context):
    connectionId = event['requestContext']['ConnectionID']
    
    table.delete_item(
        Key={
            'ConnectionID': connectionId
        }
    )
    
    return {'statusCode': 200}