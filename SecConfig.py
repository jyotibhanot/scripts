#! /usr/bin/python
import boto
import boto3
import urllib
import hashlib
import argparse
import sys

parser = argparse.ArgumentParser(description='outputs security configuration of an AWS account')
parser.add_argument('-a', '--access_key_id', required=True, help='access key id')
parser.add_argument('-k', '--secret_access_key', required=True, help='secret access key')
parser.add_argument('-t', '--security_token', help='security token (for use with temporary security credentials)')
parser.add_argument('-r', '--role', help='role to assume')
parser.add_argument('-v', '--verbose', action="store_true", help='enable verbose mode')
parser.add_argument('-d', '--debug', action="store_true", help='enable debug mode')

args = parser.parse_args()
access_key_id = args.access_key_id
secret_access_key = args.secret_access_key
security_token = args.security_token
sts = boto.connect_sts(access_key_id, secret_access_key)

if args.role:
    assumed_role = sts.assume_role(args.role, "SecAudit")
    access_key_id = assumed_role.credentials.access_key
    secret_access_key = assumed_role.credentials.secret_key
    security_token = assumed_role.credentials.session_token


def debug(str):
    if args.debug:
        print str


def verbose(str):
    if args.verbose or args.debug:
        print str

def config_line(header, name, detail):
    return header + ", " + name + ", " + detail

def config_line_policy(header, name, detail):
    verbose("===== " + header + ":  " + name + ":  " + detail + "=====")
    verbose("=========================================================")
    return config_line(header, name, detail)

def output_lines(lines):
    lines.sort()
    for line in lines:
        print line

iam = boto.connect_iam(access_key_id, secret_access_key, security_token=security_token)
boto3_iam = boto3.client('iam', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, aws_session_token=security_token)

# IAM Roles
verbose("Getting IAM role info:")
role_policy = []
roles = iam.list_roles().list_roles_response.list_roles_result.roles
roles = []
kwargs = {}
#count = 0
while True:
   # count +=1
    resp = boto3_iam.list_roles(**kwargs)
    roles.extend(resp['Roles'])
    if resp['IsTruncated']:
        kwargs['Marker'] = resp['Marker']
    else:
        break
#print('Count = {}'.format(count))
#print(len(roles))

for role in roles:
    verbose("Role: " + role['RoleName'])
    # Policy controling use of the role (always present)
    role_policy.append(config_line_policy("iam:assumerolepolicy", role['RoleName'], role['Arn']))

    #Policies around what the assumed role can do
    policies = iam.list_role_policies(role['RoleName'])
    policies = policies.list_role_policies_response.list_role_policies_result.policy_names
    for policy_name in policies:
        policy = iam.get_role_policy(role['RoleName'], policy_name)
        role_policy.append(config_line_policy("iam:rolepolicy", role['RoleName'], policy_name))
    debug(policies)
output_lines(role_policy)
