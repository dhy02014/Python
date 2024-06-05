import time
import boto3
import pandas as pd
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
        _ec2_client = RoleSession('ec2')
        self._paginator_obj = {}
        for i in _ec2_client.session_obj.keys():
            self._paginator_obj[i] = _ec2_client.session_obj[i].get_paginator('describe_instances')

    def ec2_describe(self):
        for i in self._paginator_obj:
            response_iterator = self._paginator_obj[i].paginate(
                PaginationConfig={
                    'PageSize': 10
                }
            )
            for page in response_iterator:
                print(len(page['Reservations']))
                #print(dumps(page['Reservations'][1]['Instances'], indent=4, default=str))


test = EC2Handle()
test.ec2_describe()