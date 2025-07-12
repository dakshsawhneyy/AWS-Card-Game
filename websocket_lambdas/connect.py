import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Connections')

def lambda_handler(event,context):
    connectionId = event['requestContext']['ConnectionID']  # fetch from requestContext
    
    # save connectionId to table i.e. update table
    table.put_item(
        Item = {
            'ConnectionID' : connectionId
        }
    )
    
    return {'statusCode': 200}