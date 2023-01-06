import boto3
import json


"""
Initialize your variables
"""

dynamodb = ""
s3_client = ""

table = dynamodb.Table("customers")

def lambda_handler(event, context):

    """

    :param event: contains information about the bucket name and file name
    :param context:
    :return: None

    this function allow to read json file following its insertion in the bucket
    and put the items in the table customers
    """

