import boto3
import os
from boto3 import session
from botocore.client import Config
from boto3.s3.transfer import S3Transfer
from digiinsurance import settings


# Initiate session

def get_s3_client():
    # """A client object is used to access boto3 low-level
    #    interface (close to 1:1 map with AWS API)"""
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='nyc3', #enter your own region_name
                            endpoint_url='https://nyc3.digitaloceanspaces.com', #enter your own endpoint url
                            aws_access_key_id= settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY)
    return client

# def get_s3_resource():
#     # """A resource object is used to access boto3 high-level objects
#     #   (easier to work with than client but less powerful)"""
#     session = get_s3_session()
#     return session.resource('s3')


def get_s3_bucket():
    s3 = get_s3_resource()
    return s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME)