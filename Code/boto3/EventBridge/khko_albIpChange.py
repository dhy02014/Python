from datetime import datetime, timezone, timedelta
import json
import requests
import socket
import boto3

schedule_client = boto3.client("scheduler", region_name="ap-northeast-2")

webhook_url = {
    "TEST": "Webhook URL",
}

target_alb = {
    "TEST": "internal-HHD-AN2-COM-ALB-DEV-TEST-INT-1111111.ap-northeast-2.elb.amazonaws.com",
}

exec_date = datetime.now(timezone(timedelta(hours=9, minutes=1))).strftime("%Y-%m-%dT%H:%M")


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
                "RoleArn": "Role Arn Info"
            }
        )
    except Exception as e:
        print(e)


def send_message(event):
    try:
        svc_name = str(event["resources"]).split("-")[-2]
        change_ip = str(list(socket.gethostbyname_ex(target_alb[svc_name]))[2]).strip("[]").replace("'", "")

        if svc_name in webhook_url:
            message = {"text": f"{svc_name} ALB의 IP가 변경되었으며, 변경후 최종 IP는 아래와 같습니다.\n{change_ip}"}
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