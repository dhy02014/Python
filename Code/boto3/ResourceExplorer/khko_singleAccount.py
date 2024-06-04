import time
import boto3
import json


class SingleAccountSession:
    def __init__(self):
        with open('RoleSessionToken.json') as f:
            _data = json.load(f).get('mmc-khko')
        _client = boto3.session.Session(
            aws_access_key_id=_data.get('AccessKeyId'),
            aws_secret_access_key=_data.get('SecretAccessKey'),
            aws_session_token=_data.get('SessionToken')
        ).client('resource-explorer-2', region_name='ap-northeast-2')
        _rsc_filter = 'service:ec2'
        pagination = _client.get_paginator('search')
        page_iterator = pagination.paginate(
            MaxResults=200,
            QueryString=_rsc_filter,
        )
        for page in page_iterator:
            #print(page['Resources']))
            print(json.dumps(page, indent=4, default=str))

#        self.khko = _client.search(
#            MaxResults=2000,
#            QueryString=_rsc_filter
#        )#['Resources']


test = SingleAccountSession()
#print(json.dumps(test.khko, indent=4, default=str))