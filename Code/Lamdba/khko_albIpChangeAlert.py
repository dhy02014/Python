from datetime import datetime, timezone, timedelta
import json
import requests
import socket
import boto3

schedule_client = boto3.client("scheduler", region_name="ap-northeast-2")

webhook_url = {
    "TEST": "Test Webhook URL",
    "KHH": "Test Webhook URL",
    "KHKO": "Test Webhook URL"
}

target_alb = {
    "TEST": "internal-ALB-DEV-TEST-INT-1111111.ap-northeast-2.elb.amazonaws.com",
    "KHKO": "internal-ALB-DEV-TEST-INT-1111111.ap-northeast-2.elb.amazonaws.com",
    "KKH": "internal-ALB-DEV-TEST-INT-1111111.ap-northeast-2.elb.amazonaws.com",
}

svc_int_domain = {
    "TEST": ["testdev.test.com", "khkodev.test.com"],
    "KHKO": "khkodev.test.com",
    "KKH": ["kkhdev.test.com", "khko2dev.test.com"],
}

exec_date = datetime.now(timezone(timedelta(hours=9, minutes=12))).strftime("%Y-%m-%dT%H:%M")


def create_event_scheduler(event):
    try:
        svc_alb = event["detail"]["requestParameters"]["description"].split("/")[1]
        schedule = schedule_client.create_schedule(
            ActionAfterCompletion='DELETE',
            FlexibleTimeWindow={"Mode": "OFF"},
            Name=svc_alb,
            ScheduleExpression=f"at({exec_date})",
            ScheduleExpressionTimezone="Asia/Seoul",
            Target={
                "Arn": "Arn Info",
                "RoleArn": "Scheduler Role Arn Info"
            }
        )
    except Exception as e:
        print(e)


def send_message(event):
    try:
        svc_name = str(event["resources"]).split("-")[-2]
        change_ip = str(list(socket.gethostbyname_ex(target_alb[svc_name]))[2]).strip("[],").replace("'", "")

        if isinstance(svc_int_domain[svc_name], list) and svc_name in webhook_url:
            entries = "\n".join([f"{change_ip}\t{domain}" for domain in svc_int_domain[svc_name]])
            message = {"text": f"{svc_name} ALB의 IP가 변경되었으며, 변경후 최종 IP는 아래와 같습니다.\n{entries}"}
            response = requests.post(webhook_url[svc_name], json=message,
                                     headers={'Content-Type': 'application/json; chartset=UTF-8'})

        elif svc_name in webhook_url:
            entries = "\n".join([f"{change_ip}\t{svc_int_domain[svc_name]}"])
            message = {"text": f"{svc_name} ALB의 IP가 변경되었으며, 변경후 최종 IP는 아래와 같습니다.\n{entries}"}
            response = requests.post(webhook_url[svc_name], json=message,
                                     headers={'Content-Type': 'application/json; chartset=UTF-8'})

            if response.status_code == 200:
                print('메시지가 발송 성공')
            else:
                print(f'메시지 발송 실패: {response.status_code}, {response.text}')
    except Exception as e:
        print(e)


def lambda_handler(event, context):
    if not event["resources"]:
        create_event_scheduler(event)
    else:
        send_message(event)