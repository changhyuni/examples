# config.py

# AWS 설정
AWS_REGION = 'us-east-1'  # 필요한 리전으로 변경
LAMBDA_FUNCTION_NAME = 'IAMUserMonitor'
EVENT_RULE_NAME = 'IAMUserEventsRule'
ROLE_NAME = 'LambdaIAMUserMonitorRole'

# Slack 설정
SLACK_CHANNEL = '#alert'  # 실제 Slack 채널로 변경
HOOK_URL = 'https://hooks.slack.com/services/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'  # 실제 Webhook URL로 변경
