import pandas as pd
import json
from Code.boto3.ResourceExplorer.khko_exportList import ResourceExplorerObject
from Code.boto3.Common.khko_roleSession import RoleSession
import logging

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#logger = logging.getLogger("khko_export_tag")
#logger.setLevel(logging.INFO)
#stream_handler = logging.StreamHandler()
#logger.addHandler(stream_handler)

def create_token():
    from Code.boto3.Common.khko_createSession import GetAccessInfo
    token = GetAccessInfo()
    token.get_assume_role()
    print(f"{token._key} Account RoleToken 발급 완료")
#create_token()

'''
def eks_test():
    _client = RoleSession('eks')
    _cluster_list = _client.session_obj['mmc-khko'].list_clusters()
    for i in _cluster_list['clusters']:
        if 'khko' in i:
            print(i)
        #print(json.dumps(cluster_list['clusters'], indent=4, default=str))
#eks_test()
'''

def ec2_test():
    _client = RoleSession('ec2')
    paginator = _client.session_obj['mmc-khko'].get_paginator('describe_instances')
    _list = paginator.paginate(
        Filters=[
            {
                'Name': 'tag:Owner',
                'Values': [
                    'khko'
                ]
            },
            {
                'Name': 'instance-state-name',
                'Values': [
                    'running'
                ]
            }
        ]
    )
    ec2_list = []
    for page in _list:
        for i in range(len(page['Reservations'])):
            #print(json.dumps(page['Reservations'][i]['Instances'][0]['Tags'], indent=4, default=str))
            ec2_list.append(page['Reservations'][i]['Instances'][0]['InstanceId'])
    return str(ec2_list).replace("'", "")
print(ec2_test())

'''
class CommonSession:
    def __init__(self):
        khko = ResourceExplorerObject()
        _rsc_filter = 'service:ec2 region:ap-northeast-2'       # 추출할 Resource Filter 정보
        self.sss = []
        for i in khko._data:
            paginator = khko._session_obj[i].get_paginator('search')
            self.page_iterator = paginator.paginate(
                MaxResults=600,
                QueryString=_rsc_filter
            )
            for page in self.page_iterator:
                print(json.dumps(page, indent=4, default=str))
                print(len(page))
                #self.sss.append(page['Resources'])
        #print(len(self.sss))

    def make_df(self):
        df = pd.DataFrame(self.sss)
        df.to_csv('result3.csv')

test = CommonSession()


def get_session_token(self):  # Access Key에 대한 Session Token 발급
    with open('AccessKeyInfo.json', 'r', encoding='utf-8') as f:  # AccessKey 정보를 가져오는 행위
        _keyinfo = json.load(f)
        _token_info = {}
        for i in self._client_obj:
            _response = i.get_session_token(
                DurationSeconds=900
            )
            _token_info[self._key.pop(0)] = _response.get('Credentials', 'Key not found')
        CreatFile.write(dumps(_token_info, indent=4, default=str))


def read_file():
    with open('AccessKeyInfo.json', 'r', encoding='utf-8') as f:  # AccessKey 정보를 가져오는 행위
        return f

def append_file():
'''