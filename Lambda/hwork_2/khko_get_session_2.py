import time
import logging
from concurrent.futures import ThreadPoolExecutor
import pyotp
import boto3
from json import dumps, load

stime = time.time()

logger = logging.getLogger("khko_get_keyinfo_2")
stream_handler = logging.StreamHandler()
logger.setLevel(logging.INFO)
logger.addHandler(stream_handler)


class GetAccessInfo:  # Session Token을 얻기 위한 Class
    def __init__(self):  # AWS API Call을 하기 위한 생성 및 초기화
        with open('AccessKeyInfo.json', 'r', encoding='utf-8') as f:  # AccessKey 정보를 가져오는 행위
            self._keyinfo = load(f)
        self._key = []  # Assume Role을 생성할 조건에 만족하는 Account를 저장
        self._client_obj = []
        for i in self._keyinfo.keys():  # Assume Role을 받기 위한 조건에 맞는 Key 확인
            if (self._keyinfo[i].get('Active') == 'Y' and self._keyinfo[i].get('AWS_ACCESS_KEY_ID')
                    and self._keyinfo[i].get('Role')):
                self._key.append(i)
                _client = boto3.Session(
                    aws_access_key_id=self._keyinfo[i].get('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=self._keyinfo[i].get('AWS_SECRET_ACCESS_KEY'),
                    aws_session_token=self._keyinfo[i].get('AWS_SESSION_TOKEN')
                ).client('sts')
                self._client_obj.append(_client)

    def get_session_token(self):  # Access Key에 대한 Session Token 발급
        with open('SessionToken.json', 'a', encoding='utf-8') as CreatFile:  # Session Token 정보 저장할 파일 지정
            CreatFile.truncate(0)
            _token_info = {}
            for i in self._client_obj:
                _response = i.get_session_token(
                    DurationSeconds=900
                )
                try:
                    _token_info[self._key.pop(0)] = _response['Credentials']
                except Exception as e:
                    print(e)
            CreatFile.write(dumps(_token_info, indent=4, default=str))

    def get_assume_role(self):  # Assume Role에 대한 Session Token 발급
        with open('RoleSessionToken.json', 'a', encoding='utf-8') as CreatFile:  # Session Token 정보 저장할 파일 지정
            CreatFile.truncate(0)
            _role_info = {}
            for i in self._key:     # Assume Role Token을 Json 파일에 저장
                _response = self._client_obj.pop(0).assume_role(
                    RoleArn=self._keyinfo[i]['Role'].get('RoleArn'),
                    RoleSessionName=self._keyinfo[i]['Role'].get('RoleSessionName'),
                    DurationSeconds=900,
                    ExternalId=self._keyinfo[i]['Role'].get('ExternalId')
                )
                _role_info[i] = _response['Credentials']
            CreatFile.write(dumps(_role_info, indent=4, default=str))
            #print(dumps(_role_info, indent=4, default=str))

    def mfa_get_session_token(self):
        with open('SessionToken.json', 'a', encoding='utf-8') as CreatFile:  # Session Token 정보 저장할 파일 지정
            CreatFile.truncate(0)
            _token_info = {}
            for i in self._key:
                if 'MFA' in self._keyinfo[i]:
                    _otp = pyotp.TOTP(self._keyinfo[i]['MFA']['Code']).now()
                    _response = self._client_obj.pop(0).get_session_token(
                        DurationSeconds=900,
                        SerialNumber=self._keyinfo[i]['MFA'].get('SerialNumber'),
                        TokenCode=_otp
                    )
                    _token_info[self._key.pop(0)] = _response['Credentials']
            CreatFile.write(dumps(_token_info, indent=4, default=str))

#    def mfa_get_assume_role(self):
#        for i in self._key:
#            _response = self._keyinfo.client.assume_role(
#                RoleArn=self._keyinfo[i]['Role'].get('RoleArn'),
#                RoleSessionName=self._keyinfo[i]['Role'].get('RoleSessionName'),
#                DurationSeconds=900,
#                ExternalId=self._keyinfo[i]['Role'].get('ExternalId'),
#                SerialNumber=self._keyinfo.otp_info()[1]
#            )
#        with open('RoleSessionToken.json', 'w', encoding='utf-8') as CreatFile:
#            CreatFile.write(dumps(_response['Credentials'], default=str, indent=4))
#        CreatFile.write('\n')


obj = GetAccessInfo()
obj.get_session_token()


def check_time():
    print(f"{time.time() - stime:.5f} sec")


check_time()
