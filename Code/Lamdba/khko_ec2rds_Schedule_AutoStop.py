from datetime import datetime, timezone, timedelta
from json import loads, dumps
import boto3


# AWS 인터페이스
ec2_client = boto3.client("ec2", region_name="ap-northeast-2")
ec2_resource = boto3.resource("ec2", region_name="ap-northeast-2")
rds_client = boto3.client("rds", region_name="ap-northeast-2")
schedule_client = boto3.client("scheduler", region_name="ap-northeast-2")

now_date = datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d")

# Schedule 설정 대상 EC2 List
ec2_list = []
schedule_list = {}


def autostop_ec2_find_v2():
    for i in ec2_resource.instances.all():
        if "running" == i.state["Name"] and "DEV" in str(i.tags):
            for tag in i.tags:
                if tag["Key"] == "Schedule":
                    schedule_list[i.id] = f"{tag['Value'].split('_')[0]}T{tag['Value'].split('_')[1]}"
                if tag["Key"] == "AutoStop" and tag["Value"].upper() == "Y" and now_date not in str(i.tags):
                    ec2_list.append(i.id)
    ec2_create_event_scheduler()

def ec2_create_event_scheduler():
    for t_ec2 in schedule_list:
        try:
            schedule = schedule_client.create_schedule(
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
            print(schedule)
        except Exception as e:
            print(e)


# Schedule 설정 대상 RDS List
rds_list = []

# AutoStop 대상 RDS 찾기
def autostop_rds_find():
    get_rds = rds_client.describe_db_instances()["DBInstances"]
    for i in get_rds:
        for n in i["TagList"]:
            if n["Key"] == "AutoStart" and n["Value"].upper() == "Y":
                if i["DBInstanceStatus"] == "available":
                    rds_list.append(i["DBInstanceIdentifier"])


# Lambda Handler 통한 EC2, RDS Start 수행
def lambda_handler(event, context):
  autostop_ec2_find_v2()
  for target_ec2 in ec2_list:
      ec2_client.stop_instances(InstanceIds=[target_ec2])
  autostop_rds_find()
  for target_rds in rds_list:
      rds_client.stop_db_instance(DBInstanceIdentifier=target_rds)