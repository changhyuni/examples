# lambda_setup.py

import boto3
import zipfile
from io import BytesIO
import json
from botocore.exceptions import ClientError

from utils import generate_unique_suffix

def create_zip_from_code(file_path):
    """지정된 파일을 읽어 ZIP 파일을 생성하여 반환합니다."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        with open(file_path, 'r') as f:
            zf.writestr('lambda_function.py', f.read())
    zip_buffer.seek(0)
    return zip_buffer.read()

def create_lambda_function(lambda_client, function_name, role_arn, code_file_path, handler='lambda_function.lambda_handler', runtime='python3.11', environment=None):
    # Lambda 코드 zip 압축
    try:
        zip_bytes = create_zip_from_code(code_file_path)
    except Exception as e:
        print(f"Error zipping Lambda code: {e}")
        return None

    try:
        response = lambda_client.create_function(
            FunctionName=function_name,
            Runtime=runtime,
            Role=role_arn,
            Handler=handler,
            Code={'ZipFile': zip_bytes},
            Description='Lambda function to monitor IAM user creation/deletion and send Slack messages',
            Timeout=15,
            MemorySize=128,
            Publish=True,
            Environment={
                'Variables': environment if environment else {}
            }
        )
        function_arn = response['FunctionArn']
        print(f"Lambda function '{function_name}' created with ARN: {function_arn}")
    except lambda_client.exceptions.ResourceConflictException:
        response = lambda_client.get_function(FunctionName=function_name)
        function_arn = response['Configuration']['FunctionArn']
        print(f"Lambda function '{function_name}' already exists with ARN: {function_arn}")
    except ClientError as e:
        print(f"Error creating Lambda function: {e}")
        return None

    return function_arn
