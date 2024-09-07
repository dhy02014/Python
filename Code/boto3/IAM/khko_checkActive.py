import time
import boto3
from json import load, dumps
from Code.boto3.Common.khko_roleSession import RoleSession

def create_token():
    from Code.boto3.Common.khko_createSession import GetAccessInfo
    token = GetAccessInfo()
    token.get_assume_role()
    print(f"{token._key} Account RoleToken 발급 완료")
#create_token()

class EC2Handle:
    def __init__(self):
        iam_client = RoleSession('iam')
        self._paginator_obj = {}
        for i in iam_client.session_obj.keys():
            self._paginator_obj[i] = iam_client.session_obj[i].get_paginator('describe_instances')
