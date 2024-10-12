# iam_setup.py

import boto3
import json
from botocore.exceptions import ClientError

def create_iam_role(iam_client, role_name):
    assume_role_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }

    try:
        response = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy),
            Description='Role for Lambda function to monitor IAM user creation/deletion and send Slack messages'
        )
        role_arn = response['Role']['Arn']
        print(f"IAM Role '{role_name}' created with ARN: {role_arn}")
    except iam_client.exceptions.EntityAlreadyExistsException:
        response = iam_client.get_role(RoleName=role_name)
        role_arn = response['Role']['Arn']
        print(f"IAM Role '{role_name}' already exists with ARN: {role_arn}")
    except ClientError as e:
        print(f"Error creating IAM role: {e}")
        raise

    # 정책 첨부
    try:
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn='arn:aws:iam::aws:policy/CloudWatchLogsFullAccess'
        )
        print(f"Policies attached to role '{role_name}'.")
    except ClientError as e:
        print(f"Error attaching policies to role: {e}")
        raise

    return role_arn
