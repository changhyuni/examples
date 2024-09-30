import boto3

# 세션 생성
session = boto3.Session

# IAM 클라이언트 생성
iam = session.client('iam')

# IAM 사용자 생성
response = iam.create_user(
    UserName='user-sdk'  # 생성할 사용자의 이름
)

# 생성된 사용자의 정보 출력
print(f"IAM 사용자 생성 완료: {response['User']['UserName']}")