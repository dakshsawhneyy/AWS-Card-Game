import boto3

dynamodb = boto3.client('dynamodb')

# In creation of table, only initialize unique identifier of the table
dynamodb.create_table(
    TableName='GameSession',   
    KeySchema=[
        { 'AttributeName': 'GameID', 'KeyType': 'HASH' },  # Unique HASH key
    ],
    AttributeDefinitions=[
        { 'AttributeName': 'GameID', 'AttributeType': 'S' },  # String type
    ],  
    ProvisionedThroughput={     # Capacity to provision  # Cost Optimization
        'ReadCapacityUnits': 5,     # 5 read/write per second
        'WriteCapacityUnits': 5
    }
)

dynamodb.create_table(
    TableName='Players',
    KeySchema=[
        { 'AttributeName': 'PlayerID', 'KeyType': 'HASH' },  # Unique HASH key
    ],
    AttributeDefinitions=[
        { 'AttributeName': 'PlayerID', 'AttributeType': 'S' },  # String type
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,     # 5 read/write per second
        'WriteCapacityUnits': 5
    }
)

dynamodb.create_table(
    TableName='Cards',
    KeySchema=[
        { 'AttributeName': 'CardID', 'KeyType': 'HASH' },  # Unique HASH key
    ],
    AttributeDefinitions=[
        { 'AttributeName': 'CardID', 'AttributeType': 'S' },  # String type
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,     # 5 read/write per second
        'WriteCapacityUnits': 5
    }
)