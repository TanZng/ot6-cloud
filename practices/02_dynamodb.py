import boto3
import pandas as pd

from decimal import Decimal


def createTable(db):
    table = db.create_table(
        TableName='toys',
        KeySchema=[
            {
                'AttributeName': 'Number',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'Number',
                'AttributeType': 'N'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.wait_until_exists()

    # Print out some data about the table.
    print(table.item_count)    
    
    return table

def insertItem(table, item):
    response = table.put_item(
        Item={
        'Number': item.Number,
        'City': item.City,
        'Gender': item.Gender,
        'Age': item.Age,
        'Income': Decimal(item.Income),
        'Illness': item.Illness,
        }
    )
    print(response)

def queryItem(table, index):
    response = table.get_item(
    Key={
        'Number': index
    }
    )
    item = response['Item']
    print(item)

def updateAge(table, index, age):
    table.update_item(
    Key={
        'Number': index
    },
    UpdateExpression='SET Age = :val1',
    ExpressionAttributeValues={
        ':val1': age
    }
)

dynamodb = boto3.resource('dynamodb')

table = createTable(dynamodb)
#table = dynamodb.Table('toys')


df = pd.read_csv('toy_dataset.csv')
df = df.head(5)

for index, row in df.iterrows():
    insertItem(table, row)
    print(index)

queryItem(table, 15)
updateAge(table, 15, 3)
queryItem(table, 15)