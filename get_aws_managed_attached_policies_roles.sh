#! /bin/bash

aws iam list-roles | jq -r '.Roles[].RoleName' | while IFS= read -r role; do aws iam list-attached-role-policies --role-name "$role" | jq -r --arg role "$role" '.AttachedPolicies[] | [$role, .PolicyName, .PolicyArn] | @csv'; done > attached_policies.csv
