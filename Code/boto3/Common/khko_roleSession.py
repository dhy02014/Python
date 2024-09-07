import boto3
from json import load, dumps
from Code.boto3.Common import khko_fileHandle


def create_token():
    from Code.boto3.Common.khko_createSession import GetAccessInfo
    token = GetAccessInfo()
    token.get_assume_role()
    print(f"{token._key} Account RoleToken 발급 완료")
#create_token()


class RoleSession:
    def __init__(self, service_name):
        _file_obj = khko_fileHandle.FileHandle()
        _data = _file_obj.read_rolefile()
        self.session_obj = {}  # Dict 형태로 Client Session Object 저장 용도
        for i in _data.keys():
            _session = boto3.session.Session(
                aws_access_key_id=_data[i].get('AccessKeyId', 'AccessKey does not exist'),
                aws_secret_access_key=_data[i].get('SecretAccessKey', 'SecretAccessKey does not exist'),
                aws_session_token=_data[i].get('SessionToken', 'SessionToken does not exist'),
            ).client(service_name, region_name='ap-northeast-2')
            self.session_obj[i] = _session

#tmp = RoleSession('resource-explorer-2')