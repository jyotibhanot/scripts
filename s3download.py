#! /usr/bin/env python
# Author : jyoti.bhanot30@gmail.com
import sys
import os
import boto3
import botocore
import re
import collections
import urllib3

# to supress warnings into console
urllib3.disable_warnings()

# to get boto3 session using aws credentials
def get_session(aws_access_key_id, aws_secret_access_key):
  session = boto3.Session(
      aws_access_key_id = aws_access_key_id.strip('\n'),
      aws_secret_access_key = aws_secret_access_key.strip('\n'),
  )
  return session

# this function downloads files from s3 bucket.
def download_files(files, bucket, aws_access_key_id, aws_secret_access_key):
  session = get_session(aws_access_key_id, aws_secret_access_key)
  s3 = session.resource('s3')
  for file in files:
    if os.path.exists(file):
       print "Skipping download.File already exists."
       sys.exit(0) 
    try:
        s3.Bucket(bucket).download_file(file, os.path.basename(file))
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

def main():
  files = [] # For multiple files
  bucket = 'onlinesales-coding-test'
  aws_access_key_id = raw_input("aws_access_key_id : ")
  aws_secret_access_key = raw_input("aws_secret_access_key : ")
  s3_file_name = raw_input("s3_file_name : ")
  files.append(s3_file_name)
  download_files(files, bucket, aws_access_key_id, aws_secret_access_key)
   
if __name__ == '__main__':
  main()
