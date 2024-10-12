# main.py

import boto3
from botocore.exceptions import ClientError
import sys

from config import (
    AWS_REGION,
    LAMBDA_FUNCTION_NAME,
    EVENT_RULE_NAME,
    ROLE_NAME,
    SLACK_CHANNEL,
    HOOK_URL,
)
from utils import generate_unique_suffix
from iam import create_iam_role
from lambda_function import create_lambda_function
from eventbridge import create_eventbridge_rule, add_permission_to_lambda, create_event_target

def main():
    # AWS 클라이언트 초기화
    event_client = boto3.client('events', region_name=AWS_REGION)
    lambda_client = boto3.client('lambda', region_name=AWS_REGION)
    iam_client = boto3.client('iam')
    sts_client = boto3.client('sts')

    # AWS 계정 ID 가져오기
    try:
        account_id = sts_client.get_caller_identity()["Account"]
        print(f"AWS Account ID: {account_id}")
    except ClientError as e:
        print(f"Error getting AWS account ID: {e}")
        sys.exit(1)

    # Step 1: IAM Role 생성 및 정책 첨부
    role_arn = create_iam_role(iam_client, ROLE_NAME)

    # Step 2: Lambda 함수 생성
    function_arn = create_lambda_function(
        lambda_client=lambda_client,
        function_name=LAMBDA_FUNCTION_NAME,
        role_arn=role_arn,
        code_file_path='lambda_code/lambda_function.py',
        environment={
            'SLACK_CHANNEL': SLACK_CHANNEL,
            'HOOK_URL': HOOK_URL
        }
    )
    if not function_arn:
        print("Lambda 함수 생성 실패. 스크립트를 종료합니다.")
        sys.exit(1)

    # Step 3: EventBridge 규칙 생성
    event_pattern = {
        "source": ["aws.iam"],
        "detail-type": ["AWS API Call via CloudTrail"],
        "detail": {
            "eventSource": ["iam.amazonaws.com"],
            "eventName": ["CreateUser", "DeleteUser"]
        }
    }
    rule_arn = create_eventbridge_rule(event_client, EVENT_RULE_NAME, event_pattern)
    if not rule_arn:
        print("EventBridge 규칙 생성 실패. 스크립트를 종료합니다.")
        sys.exit(1)

    # Step 4: Lambda 함수에 권한 추가
    add_permission_to_lambda(lambda_client, LAMBDA_FUNCTION_NAME, rule_arn)

    # Step 5: EventBridge 규칙에 Lambda 함수 대상 추가
    create_event_target(event_client, EVENT_RULE_NAME, function_arn)

    print("AWS 리소스 설정이 완료되었습니다.")

if __name__ == '__main__':
    main()
