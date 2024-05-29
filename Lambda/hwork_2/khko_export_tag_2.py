import time
import logging
import json
import boto3
from pandas import DataFrame
from khko_get_session_2 import AccessInfo


create_token = AccessInfo()
create_token.get_assume_role()


def get_role():
    # with open("H:/내 드라이브/Code/assume_Credential.json", 'r', encoding='utf-8') as f:
    with open("assume_Credential.json", 'r', encoding='utf-8') as f:
        data = list(json.load(f).values())
    return data


logger = logging.getLogger("khko_export_tag_2")
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)


role_info = get_role()
session = boto3.session.Session(
    aws_access_key_id=role_info[0],
    aws_secret_access_key=role_info[1],
    aws_session_token=role_info[2]
).client('resource-explorer-2', region_name='ap-northeast-2')


rg = 'service:ec2 region:ap-northeast-2'
#rg = 'accountid:485615454673'


class ResourceExplorerObject:
    def __init__(self):
        _rexp_session = session
        self.box = _rexp_session.search(
            MaxResults=1000,
            QueryString=rg
        )['Resources']
        for i in range(len(self.box)):
            if len(self.box[i]['Properties']) > 0:
                n = len(self.box[i]['Properties'][0]['Data'])
                _tags = []
                for t in range(n):
                    _tags.append(self.box[i]['Properties'][0]['Data'][t].get('Key')
                                 + ": "
                                 + self.box[i]['Properties'][0]['Data'][t].get('Value'))
                self.box[i]['Tags'] = _tags

    def chg_df(self, *colname):
        _columns = list(colname)
        rexp_df = DataFrame(self.box)[_columns].sort_values(by='LastReportedAt', ignore_index=True)
        rexp_df.to_csv('result.csv')



rsc_info = ResourceExplorerObject()
rsc_info.chg_df('ResourceType', 'Region', 'Arn', 'LastReportedAt', 'Tags')


#print(f"실행된 시간: {time.time() - start_time:.5f} sec")