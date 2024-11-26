from datetime import datetime, timezone, timedelta
from json import loads, dumps
import boto3


# AWS 인터페이스
ec2_client = boto3.client("ec2", region_name="ap-northeast-2")
ec2_resource = boto3.resource("ec2", region_name="ap-northeast-2")
rds_client = boto3.client("rds", region_name="ap-northeast-2")


# AutoStart 대상 EC2 찾기
def finding_target_ec2():
    target_ec2 = []

    for find_ec2 in ec2_resource.instances.all():
        if find_ec2.state["Name"] == "running":
            tags = find_ec2.tags or []
            if not any(tag["Key"] == "AutoStart" and tag["Value"].upper() == "Y" for tag in tags):
                target_ec2.append(find_ec2.id)
    return target_ec2

# AutoStop 대상 RDS 찾기
def autostop_rds_find():
    target_rds = []

    for find_rds in rds_client.describe_db_instances()["DBInstances"]:
        if find_rds["DBInstanceStatus"] == "available":
            if not any(tag["Key"] == "AutoStart" and tag["Value"].upper() == "Y" for tag in find_rds["TagList"]):
                target_rds.append(find_rds["DBInstanceIdentifier"])
    return target_rds

# Lambda Handler 통한 EC2 Start 수행
def lambda_handler(event, context):
    try:
        # EC2 Function
        specified_ec2 = finding_target_ec2()
        if specified_ec2:
            ec2_client.start_instances(InstanceIds=specified_ec2)
        # RDS Function
        specified_rds = autostop_rds_find()
        for target_rds in specified_rds:
            rds_client.start_db_instance(DBInstanceIdentifier=target_rds)
    except Exception as e:
        print(f"Some Error Occurred {str(e)}")