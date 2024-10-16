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

class rdsAutoStop:
    rds_list = []
    def __init__(self):
        with open("RoleSessionToken.json", "r") as RoleSessionInfo:
            sessionToken = load(RoleSessionInfo)
        self.rds_client = boto3.session.Session(
            aws_access_key_id=sessionToken["mmc-khko"]["AccessKeyId"],
            aws_session_token=sessionToken["mmc-khko"]["SessionToken"],
            aws_secret_access_key=sessionToken["mmc-khko"]["SecretAccessKey"],
        ).client("rds")

    def autostop_rds_find(self):
        get_rds = self.rds_client.describe_db_instances()["DBInstances"]
        for i in get_rds:
            #print(dumps(i, indent=4, default=str))
            for n in i["TagList"]:
                if n["Key"] == "khko" and n["Value"] == "test":
                    rds_list = []

#    def autostop_rds_find(self):
#        get_rds = self.rds_client.describe_db_instances()["DBInstances"]
#        for i in get_rds:
#            for n in i["TagList"]:
#                if i["TagList"][n]["Key"] == "AutoStop" and i["TagList"][n]["Value"].upper() == "Y":
#                    if i["DBInstanceStatus"] == "available":
#                        rds_list.append(i["DBInstanceIdentifier"])

#autostop_rds_find()
#for target_rds in rds_list:
#  rds_client.stop_db_instance(DBInstanceIdentifier=target_rds)

#tmp = rdsAutoStop()
#tmp.autostop_rds_find()