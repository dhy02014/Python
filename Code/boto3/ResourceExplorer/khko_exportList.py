import time
import logging
import boto3
from json import load, dumps
import pandas as pd


stime = time.time()


def create_token():
    from Code.boto3.Common.khko_createSession import GetAccessInfo
    token = GetAccessInfo()
    token.get_assume_role()
    print(f"{token._key} Account RoleToken 발급 완료")
#create_token()

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#logger = logging.getLogger("khko_export_tag")
#logger.setLevel(logging.INFO)
#stream_handler = logging.StreamHandler()
#logger.addHandler(stream_handler)


class ResourceExplorerObject:
    def __init__(self):
        with open("RoleSessionToken.json", 'r', encoding='utf-8') as load_file:  # File에서 Token 정보 읽어오기
            self._data = load(load_file)
            self._session_obj = {}  # Dict 형태로 Client Session Object 저장 용도
            for i in self._data.keys():
                _session = boto3.session.Session(
                    aws_access_key_id=self._data[i].get('AccessKeyId'),
                    aws_secret_access_key=self._data[i].get('SecretAccessKey'),
                    aws_session_token=self._data[i].get('SessionToken')
                ).client('resource-explorer-2', region_name='ap-northeast-2')
                self._session_obj[i] = _session

    def get_resource_list(self, *colname):
        _rsc_filter = 'service:ec2'  # 추출할 Resource Filter 정보
        _list_obj = {}  # 각 Account의 Resource 정보를 Dict 타입으로 저장
        for i in self._session_obj.keys():  # 각 Account에서 Resource Explorer API Call
            _list_obj[i] = self._session_obj[i].search(
                MaxResults=50,
                QueryString=_rsc_filter
            )['Resources']
            for n in range(len(_list_obj[i])):  # 동작을 실행할 Account 정보
                _list_obj[i][n]['AccountName'] = i
                if len(_list_obj[i][n]['Properties']) > 0:  # 추출되는 Resource들에 대한 Tag 정보 체크
                    _tags = []
                    for t in range(
                            len(_list_obj[i][n]['Properties'][0]['Data'])):  # Properties 정보를 통해 가시성 있는 Tags Column 생성
                        _tags.append(_list_obj[i][n]['Properties'][0]['Data'][t].get('Key')
                                     + ": "
                                     + _list_obj[i][n]['Properties'][0]['Data'][t].get('Value'))
                    _list_obj[i][n]['Tags'] = _tags
        return _list_obj

    def chg_df_csv(self, *colname):     # csv 파일로 Export
        _resource_list = self.get_resource_list(colname)
        _account = []
        for i in _resource_list:        # Parameter를 입력받아 Columns 정렬
            i = pd.DataFrame(_resource_list.get(i))[list(colname)].sort_values(by='LastReportedAt', ignore_index=True)
            i['ResourceType'] = i['ResourceType'].str.split(':').str[1]
            _account.append(i)
        _collect_list = pd.concat([*_account], ignore_index=True)
        _collect_list.to_csv('result.csv')

#    def chg_df_excel(self, *colname):
#        _resource_list = self.get_resource_list(colname)
#        _account = []
#        for i in _resource_list:
#            i = pd.DataFrame(_resource_list.get(i))[list(colname)]. \
#                sort_values(by='LastReportedAt', ignore_index=True)
#            _account.append(i)
#        _collect_list = pd.concat([*_account], ignore_index=True)
#        for i in _collect_list:
#            _collect_list.to_excel('result.csv', sheet_name=i, engine='xlsxwriter')

#rsc_info = ResourceExplorerObject()
#rsc_info.get_resource_list('Account', 'ResourceType', 'Region', 'Arn', 'LastReportedAt', 'Tags')
#rsc_info.chg_df_csv('OwningAccountId', 'AccountName', 'Service', 'ResourceType', 'Region', 'Arn', 'LastReportedAt', 'Tags')


def check_time():
    print(f"{time.time() - stime:.5f} sec")
#check_time()
