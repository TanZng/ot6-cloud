import boto3
import json 



dynamodb = boto3.resource('dynamodb', aws_access_key_id="/", aws_secret_access_key="/")
s3_client = boto3.client('s3',  aws_access_key_id="/", aws_secret_access_key="/")

table = dynamodb.Table("customers")

def lambda_handler(event, context):
    # read the json file
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    s3_file_name = event['Records'][0]['s3']['object']['key']
    context.get_object(Bucket= bucket_name, Key = s3_file_name)
    json_object = s3_client.get_object(Bucket= bucket_name, Key = s3_file_name)
    jsonFileContent = json_object['Body'].read()
    jsonDict = json.loads(jsonFileContent)
    table.put_item( Item = jsonDict)

    
