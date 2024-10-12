# eventbridge_setup.py

import boto3
import json
from botocore.exceptions import ClientError

def create_eventbridge_rule(event_client, rule_name, event_pattern):
    try:
        response = event_client.put_rule(
            Name=rule_name,
            EventPattern=json.dumps(event_pattern),
            State='ENABLED',
            Description='Rule to trigger Lambda on IAM CreateUser and DeleteUser events'
        )
        rule_arn = response['RuleArn']
        print(f"EventBridge rule '{rule_name}' created with ARN: {rule_arn}")
        return rule_arn
    except ClientError as e:
        print(f"Error creating EventBridge rule: {e}")
        return None

def add_permission_to_lambda(lambda_client, function_name, rule_arn, statement_id='EventBridgeInvokePermission'):
    try:
        lambda_client.add_permission(
            FunctionName=function_name,
            StatementId=statement_id,
            Action='lambda:InvokeFunction',
            Principal='events.amazonaws.com',
            SourceArn=rule_arn
        )
        print("Permission added to Lambda function for EventBridge.")
    except lambda_client.exceptions.ResourceConflictException:
        print("Permission already exists for Lambda function.")
    except ClientError as e:
        print(f"Error adding permission to Lambda function: {e}")
        raise

def create_event_target(event_client, rule_name, function_arn, target_id='1'):
    try:
        event_client.put_targets(
            Rule=rule_name,
            Targets=[{'Id': target_id, 'Arn': function_arn}]
        )
        print("Lambda function added as target to EventBridge rule.")
    except ClientError as e:
        print(f"Error adding target to EventBridge rule: {e}")
        raise
