#Python script to find the security group open to the external world

#! /usr/bin/env python
import sys
import boto
from boto import ec2
connection=ec2.connect_to_region("eu-west-1")
sg=connection.get_all_security_groups()
l = []
try:
    for securityGroup in sg:
         for rule in securityGroup.rules:
             if '0.0.0.0/0' in str(rule.grants):
   		l.append(str(securityGroup.id))
    print sorted(l)
except :
    print 'Some Error occurred : '
