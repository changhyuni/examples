import boto3

# 세션 생성
session = boto3.Session()

# IAM 클라이언트 생성
iam = session.client('iam')

# IAM 사용자 생성
response = iam.list_users()

# 생성된 사용자의 정보 출력
print(response)