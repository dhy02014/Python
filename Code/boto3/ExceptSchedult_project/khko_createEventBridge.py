from datetime import datetime, timedelta, timezone
import time
import os
import logging
import boto3
from json import load, dumps
from Code.boto3.Common.khko_roleSession import RoleSession

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#logger = logging.getLogger("khko_export_tag")
#logger.setLevel(logging.INFO)
#stream_handler = logging.StreamHandler()
#logger.addHandler(stream_handler)

# 현재 Working 디렉토리 확인
#print(os.getcwd())

def create_token():
    from Code.boto3.Common.khko_createSession import GetAccessInfo
    token = GetAccessInfo()
    token.get_assume_role()
    print(f"{token._key} Account RoleToken 발급 완료")
#create_token()


#datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
#now_date = datetime.datetime.now().strftime("%Y-%m-%d")
now_date = datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d')

ec2_list = []
schedule_list = {}

rds_list = []
rds_schedule = {}

class CreateEventSchedule:
    def __init__(self):
        with open("RoleSessionToken.json", "r") as RoleSessionInfo:
            session_token = load(RoleSessionInfo)
        self.ec2_resource = boto3.session.Session(
            aws_access_key_id=session_token["mmc-khko"]["AccessKeyId"],
            aws_session_token=session_token["mmc-khko"]["SessionToken"],
            aws_secret_access_key=session_token["mmc-khko"]["SecretAccessKey"],
        ).resource("ec2")
        self.rds_client = boto3.session.Session(
            aws_access_key_id=session_token["mmc-khko"]["AccessKeyId"],
            aws_session_token=session_token["mmc-khko"]["SessionToken"],
            aws_secret_access_key=session_token["mmc-khko"]["SecretAccessKey"],
        ).client("rds")
        self.schedule_client = boto3.session.Session(
            aws_access_key_id=session_token["mmc-khko"]["AccessKeyId"],
            aws_session_token=session_token["mmc-khko"]["SessionToken"],
            aws_secret_access_key=session_token["mmc-khko"]["SecretAccessKey"],
        ).client("scheduler")


    def autostop_ec2_find(self):
        for i in self.ec2_resource.instances.all():
            if "stopped" == i.state["Name"] and "DEV" in str(i.tags):
                for tag in i.tags:
                    if tag["Key"] == "Schedule":
                        schedule_list[i.id] = f"{tag["Value"].replace("_", "T")}"
                    if tag["Key"] == "AutoStop" and tag["Value"].upper() == "Y" and now_date not in str(i.tags):
                        ec2_list.append(i.id)
#        self.create_ec2_event_scheduler()
#        for target_ec2 in ec2_list:
#            try:
#                status = self.client.start_instances(InstanceIds=[target_ec2])
#                print(dumps(status, indent=4, default=str))
#            except Exception as e:
#                print(e)

    def create_ec2_event_scheduler(self):
        # schedule_list의 dict를 for문으로 돌리면 dict의 key 값들만 반환이 됨
        for t_ec2 in schedule_list:
            print(schedule_list[t_ec2])
            try:
                schedule = self.schedule_client.create_schedule(
                    ActionAfterCompletion='DELETE',
                    FlexibleTimeWindow={"Mode": "OFF"},
                    Name=f"{schedule_list[t_ec2].split("T")[0]}_{t_ec2}",
                    ScheduleExpression=f"at({schedule_list[t_ec2]})",
                    ScheduleExpressionTimezone="Asia/Seoul",
                    Target={
                        "Arn": "",
                        "RoleArn": ""
                    }
                )
                print(dumps(schedule["ScheduleArn"], indent=4, default=str))
            except Exception as e:
                print(e)

    def autostop_rds_find(self):
        get_rds = self.rds_client.describe_db_instances()["DBInstances"]
        for i in get_rds:
            for n in i["TagList"]:
                if n["Key"] == "AutoStop" and n["Value"].upper() == "Y" and now_date not in str(i["TagList"]):
                    rds_list.append(i["DBInstanceIdentifier"])
                if n["Key"] == "Schedule":
                    rds_schedule[i["DBInstanceIdentifier"]] = n["Value"].replace("_", "T")
        self.create_rds_event_scheduler()

    def create_rds_event_scheduler(self):
        # schedule_list의 dict를 for문으로 돌리면 dict의 key 값들만 반환이 됨
        for target_rds in rds_schedule:
            try:
                schedule = self.schedule_client.create_schedule(
                    ActionAfterCompletion='DELETE',
                    FlexibleTimeWindow={"Mode": "OFF"},
                    Name=f"{rds_schedule[target_rds].split("T")[0]}_{target_rds}",
                    ScheduleExpression=f"at({rds_schedule[target_rds]})",
                    ScheduleExpressionTimezone="Asia/Seoul",
                    Target={
                        "Arn": "",
                        "RoleArn": ""
                    }
                )
                print(dumps(schedule["ScheduleArn"], indent=4, default=str))
            except Exception as e:
                print(e)



khko = CreateEventSchedule()
khko.autostop_ec2_find()
khko.autostop_rds_find()