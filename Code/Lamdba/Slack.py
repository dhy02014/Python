import requests
import boto3
import logging

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#logger = logging.getLogger("slack")
#logger.setLevel(logging.DEBUG)
#stream_handler = logging.StreamHandler()
#logger.addHandler(stream_handler)


def create_token():
    from Code.boto3.Common.khko_createSession import GetAccessInfo
    token = GetAccessInfo()
    token.get_assume_role()
    print(f"{token._key} Account RoleToken 발급 완료")
#create_token()


# Class로 작성
class Slack:
    def __init__(self):
        self.client = boto3.client('eks')
    def search_khko_resource(self):
        cluster_list = self.client.list_clusters(
            )
        for i in cluster_list['clusters']:
            if 'khko' in i:
                url = 'https://hooks.slack.com/services/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'
                headers = {'Content-Type': 'application/json'}
                data = {
                    "text": "EKS Cluster Resource가 존재 : " + i
                }
                requests.post(url=url, headers=headers, json=data)

# Function으로 작성
def search_khko_resource():
    client = boto3.client('eks')
    cluster_list = client.list_clusters(
        )
    for i in cluster_list['clusters']:
        if 'khko' in i:
            url = 'https://hooks.slack.com/services/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'
            headers = {'Content-Type': 'application/json'}
            data = {
                "text": "EKS Cluster Resource가 존재 : " + i
            }
            requests.post(url=url, headers=headers, json=data)

def lambda_handler(event, context):
    search_khko_resource()