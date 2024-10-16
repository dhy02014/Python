import time
import os
import boto3
from json import load, dumps
from Code.boto3.Common.khko_roleSession import RoleSession

# 현재 Working 디렉토리 확인
#print(os.getcwd())

def create_token():
    from Code.boto3.Common.khko_createSession import GetAccessInfo
    token = GetAccessInfo()
    token.get_assume_role()
    print(f"{token._key} Account RoleToken 발급 완료")
#create_token()

ec2_list = []

class ec2AutoStop:
    def __init__(self):
        with open("RoleSessionToken.json", "r") as RoleSessionInfo:
            sessionToken = load(RoleSessionInfo)
        self.resource = boto3.session.Session(
            aws_access_key_id=sessionToken["mmc-khko"]["AccessKeyId"],
            aws_session_token=sessionToken["mmc-khko"]["SessionToken"],
            aws_secret_access_key=sessionToken["mmc-khko"]["SecretAccessKey"],
        ).resource("ec2")
        self.client = boto3.session.Session(
            aws_access_key_id=sessionToken["mmc-khko"]["AccessKeyId"],
            aws_session_token=sessionToken["mmc-khko"]["SessionToken"],
            aws_secret_access_key=sessionToken["mmc-khko"]["SecretAccessKey"],
        ).client("ec2")

    def autostop_ec2_find(self):
        for i in self.resource.instances.all():
            if "stopped" == i.state["Name"] and "DEV" in str(i.tags):
                for tag in i.tags:
                    if tag["Key"] == "AutoStop" and tag["Value"].upper() == "Y":
                        ec2_list.append(i.id)
        print(ec2_list)
#        for target_ec2 in ec2_list:
#            try:
#                status = self.client.start_instances(InstanceIds=[target_ec2])
#                print(dumps(status, indent=4, default=str))
#            except Exception as e:
#                print(e)

# Resource 인터페이스로 Instnace 정보를 가져오므로 미사용
#    def client_list_instances(self):
#        pagination = self.client.get_paginator("describe_instances")
#        for i in pagination.paginate(
#            Filters=[
#               {
#                   "Name": "instance-state-name",
#                   "Values": ["running"]
#               }
#            ],
#            paginationConfig={"MaxResults": 10}
#        ):
#            print(dumps(i, indent=4, default=str))




tmp = ec2AutoStop()
tmp.autostop_ec2_find()
