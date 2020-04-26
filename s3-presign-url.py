#! /usr/bin/python
#Author: Jyoti Bhanot <jyoti.bhanot30@gmail.com>
#This script generates S3 object pre-signed URL

#! /usr/bin/python

import logging
import boto3
import pathlib
import argparse
from botocore.exceptions import ClientError

parser = argparse.ArgumentParser(description='generates a presigned S3 object URL')
parser.add_argument('-b', '--bucket_name', required=True, help='bucket name')
parser.add_argument('-d', '--database_name', required=True, help='database name')

args = parser.parse_args()
bucket_name = args.bucket_name
database_name = args.database_name

def keys(bucket_name, prefix="", delimiter="/"):
    """Generate a key listings
    :param bucket_name: string
    :param prefix: string
    :param delimiter: string
    """
    for page in (
        boto3.client("s3")
        .get_paginator("list_objects_v2")
        .paginate(
            Bucket=bucket_name,
            Prefix=prefix[len(delimiter) :] if prefix.startswith(delimiter) else prefix,
            **{"StartAfter": prefix} if prefix.endswith(delimiter) else {}
        )
    ):
        for content in page.get("Contents", ()):
            yield content["Key"]

def latest(bucket_name, database_name):
    """Generate a latest logfile
    :param bucket_name: string
    :param database_name: string
    :return: Object keys
    """
    return(max(i for i in keys(bucket_name) if database_name in i))

def create_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 object
    s3_client = boto3.session.Session(
        region_name=boto3.client('s3').get_bucket_location(Bucket=bucket_name)["LocationConstraint"]
    ).client("s3")
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

if __name__ == "__main__":
    pathlib.Path("../s3_presigned_url").write_text(
        create_presigned_url(bucket_name, latest(bucket_name, database_name))
    )
    
print(pathlib.Path("../s3_presigned_url").read_text())

