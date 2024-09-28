#!/bin/bash

# MFA가 적용된 프로파일을 설정합니다.
SOURCE_PROFILE="default"
MFA_PROFILE="mfa"

# credentials 파일에서 MFA 디바이스 ARN을 읽어옵니다.
MFA_DEVICE_ARN=$(aws configure get mfa_arn --profile $SOURCE_PROFILE)
if [ -z "$MFA_DEVICE_ARN" ]; then
  echo "Error: MFA device ARN not found in the ~/.aws/credentials file for profile $SOURCE_PROFILE"
  exit 1
fi

# 사용자에게 MFA 코드 입력을 요청합니다.
echo "Enter your MFA token code:"
read MFA_CODE

# 임시 자격 증명 요청
CREDENTIALS=$(aws sts get-session-token \
  --serial-number "$MFA_DEVICE_ARN" \
  --token-code "$MFA_CODE" \
  --profile "$SOURCE_PROFILE" \
  --output json \
  --duration-seconds 3600)

# 요청이 실패했을 경우 오류 메시지 출력
if [ $? -ne 0 ]; then
  echo "Error: Failed to obtain temporary credentials. Please check your MFA token code and try again."
  exit 1
fi

# JSON 응답에서 자격 증명 추출
ACCESS_KEY=$(echo "$CREDENTIALS" | jq -r '.Credentials.AccessKeyId')
SECRET_KEY=$(echo "$CREDENTIALS" | jq -r '.Credentials.SecretAccessKey')
SESSION_TOKEN=$(echo "$CREDENTIALS" | jq -r '.Credentials.SessionToken')
EXPIRATION=$(echo "$CREDENTIALS" | jq -r '.Credentials.Expiration')

# 자격 증명이 제대로 추출되지 않은 경우 오류 메시지 출력
if [ -z "$ACCESS_KEY" ] || [ -z "$SECRET_KEY" ] || [ -z "$SESSION_TOKEN" ]; then
  echo "Error: Failed to parse temporary credentials. Please try again."
  exit 1
fi

# 임시 자격 증명을 MFA 프로파일에 저장
aws configure set aws_access_key_id "$ACCESS_KEY" --profile "$MFA_PROFILE"
aws configure set aws_secret_access_key "$SECRET_KEY" --profile "$MFA_PROFILE"
aws configure set aws_session_token "$SESSION_TOKEN" --profile "$MFA_PROFILE"

# MFA 토큰이 만료되는 시간 알림
echo "Temporary credentials have been set for the '$MFA_PROFILE' profile. They will expire on $EXPIRATION."