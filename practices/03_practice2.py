import boto3
import uuid
import os
from dotenv import load_dotenv
import pandas as pd

def create_bucket_name(bucket_prefix):
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_prefix, s3_resource):
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_resource.create_bucket(Bucket=bucket_name)
    return bucket_name, bucket_response

def get_buckets(s3_client):
    response = s3_client.list_buckets()
    bucket_data = ""
    bucket_4_results = ""
    for bucket in response['Buckets']:
        if "bucket-4-results" in bucket["Name"]:
            bucket_4_results = bucket["Name"]
        elif "bucket-data" in bucket["Name"]:
            bucket_data = bucket["Name"]
    return bucket_data, bucket_4_results


def push_file(client_bucket_name, file_name, file_name_key, s3_resource):
    s3_resource.Bucket(client_bucket_name).upload_file(Filename = file_name, Key = file_name_key)


def get_from_s3(s3_client, bucket_name, file_name, sql_expression):
    resp = s3_client.select_object_content(
        Bucket = bucket_name,
        Key = file_name,
        Expression = sql_expression,
        ExpressionType = 'SQL',
        InputSerialization = {'CSV': {'FileHeaderInfo': 'Use'}},
        OutputSerialization = {'CSV': {}}
    )
    file1 = open(CSV_RESULTS,"a")
    for event in resp['Payload']:
        if 'Records' in event:
            tmp = event['Records']['Payload'].decode()
            file1.write(tmp)
            print(event['Records']['Payload'].decode())
    
    file1.close()

CSV_DATA = "data/level_crime.csv"
CSV_RESULTS = "data/results.csv"
SQL_QUERY = "SELECT * from S3Object LIMIT 4"

def main():
    load_dotenv()

    SECRET_ACCESS_KEY = os.getenv('SECRET_ACCESS_KEY')
    ACCESS_KEY_ID = os.getenv('ACCESS_KEY_ID')
    REGION_NAME = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

    session = boto3.Session(
        aws_secret_access_key=SECRET_ACCESS_KEY,
        aws_access_key_id=ACCESS_KEY_ID,
        region_name=REGION_NAME
    )

    s3_resource = session.resource('s3')
    s3_client = session.client('s3')

    bucket_data, bucket_4_results = get_buckets(s3_client)

    if bucket_4_results == "" :
        bucket_4_results, ig=create_bucket("bucket-4-results",s3_resource)
    if bucket_data == "":
        bucket_data, ig=create_bucket("bucket-data",s3_resource)
        push_file(bucket_data, CSV_DATA, "level.csv",s3_resource)

    print("bucket date: ", bucket_data)
    print("bucket 4 res: ", bucket_4_results)

    # s3_client, bucket_name, file_name, sql_expression
    get_from_s3(s3_client, bucket_data, "level.csv", SQL_QUERY)

    push_file(bucket_4_results, CSV_RESULTS, "results.csv", s3_resource)

main()
