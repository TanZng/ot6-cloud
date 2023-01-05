import boto3
from ec2_metadata import ec2_metadata


def get_buckets(s3_client):
    response = s3_client.list_buckets()
    project_bucket = ""
    for bucket in response['Buckets']:
        if "project-s3" in bucket["Name"]:
            project_bucket = bucket["Name"]
    return project_bucket


def main():
    session = boto3.Session(region_name=ec2_metadata.region)

    s3_client = session.client('s3')
    bucket_data, bucket_4_results = get_buckets(s3_client)


main()