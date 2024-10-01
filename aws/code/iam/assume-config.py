import boto3

# Assume Role 프로필을 사용하여 세션 생성
session = boto3.Session(profile_name="assume")
print(session.get_credentials().get_frozen_credentials())