import boto3

# 기본 세션 생성
session = boto3.Session()
print(session.get_credentials().get_frozen_credentials())

# STS 클라이언트를 생성하여 AssumeRole 호출
sts_client = session.client('sts')
response = sts_client.assume_role(
    RoleArn="arn:aws:iam::{ACCOUNT}:role/S3DeleteRole",  # Assume할 역할의 ARN
    RoleSessionName="S3DeleteSession"
)

# AssumeRole을 통해 얻은 임시 자격증명을 사용하여 새로운 세션 생성
assumed_session = boto3.Session(
    aws_access_key_id=response['Credentials']['AccessKeyId'],
    aws_secret_access_key=response['Credentials']['SecretAccessKey'],
    aws_session_token=response['Credentials']['SessionToken']
)

print(assumed_session.get_credentials().get_frozen_credentials())

# 임시 자격증명을 사용한 S3 클라이언트 생성
s3_client = assumed_session.client('s3')

# 삭제할 S3 버킷 이름
bucket_name = 'fastcampusjune1'

# S3 버킷 삭제
s3_client.delete_bucket(Bucket=bucket_name)

print(f"S3 Bucket '{bucket_name}' has been deleted.")