[sts]
aws sts assume-role \
--role-arn arn:aws:iam::{ACCOUNT_NUMBER}:role/S3DeleteRole \
--role-session-name testman \
--duration-seconds 900

[profile]
aws configure set --profile s3 aws_access_key_id [AccessKeyId]
aws configure set --profile s3 aws_secret_access_key [SecretAccessKey]
aws configure set --profile s3 aws_session_token [SessionToken]

[s3]
aws s3 rb s3://{Bucket_NAME} --profile s3