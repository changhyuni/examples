# lambda_code/lambda_function.py

import boto3
import json
import logging
import os

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# 환경 변수에서 값 가져오기
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']
HOOK_URL = os.environ['HOOK_URL']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def send_message(message):
    req = Request(HOOK_URL, data=json.dumps(message).encode('utf-8'), headers={'Content-Type': 'application/json'})
    try:
        response = urlopen(req)
        response.read()
        logger.info("Message posted to %s", SLACK_CHANNEL)
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)

def lambda_handler(event, context):
    detail = event['detail']
    person = detail['userIdentity']['userName']
    event_time = detail['eventTime']
    event_name = detail['eventName']
    source_ip = detail['sourceIPAddress']
    iam_user = detail['requestParameters']['userName']
    
    logger.info("Event: %s", event)
    logger.info("SLACK Channel: #%s", SLACK_CHANNEL)
    logger.info("HOOK URL: %s", HOOK_URL)
    
    color = "#eb4034" if "delete" in event_name.lower() else "#0c3f7d"
    
    slack_message = {
        "channel": SLACK_CHANNEL,
        "attachments": [{
            "color": color,
            "blocks": [
                {
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f'*이벤트 이름:*\n{event_name}'},
                        {"type": "mrkdwn", "text": f'*이벤트 시간:*\n{event_time}'}
                    ]
                }
            ]
        }],
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f'소스 IP: *{source_ip}*, 수행자: *{person}*\n사용자: *{iam_user}* 에게 *{event_name}* 이벤트가 발생하였습니다.'
                }
            },
            {"type": "divider"}
        ]
    }
    
    send_message(slack_message)
