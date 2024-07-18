import requests
import random
import os
import boto3
from Code.boto3.Common.khko_roleSession import RoleSession
import json

def create_token():
    from Code.boto3.Common.khko_createSession import GetAccessInfo
    token = GetAccessInfo()
    token.get_assume_role()
    print(f"{token._key} Account RoleToken 발급 완료")
#create_token()


slack_url = os.environ['slack_url']
client = RoleSession('lambda')
p_menu = client.session_obj['mmc-khko'].get_function_configuration(
    FunctionName='khko-lambda-test'
    )['Environment']['Variables']


menu = ['김치찌개', '햄버거', '중식', '돈까스', '부대찌개', '김밥천국', '명동칼국수', '국밥', '뼈해장국', '마제소바']
past_menu = p_menu['past_menu']
lp_menu = past_menu.split(', ')
print(lp_menu)
if past_menu:
    for i in lp_menu:
        menu.remove(i)

today_menu = random.choice(menu)
lp_menu.pop(0)
lp_menu.append(today_menu)
sr_menu = str(lp_menu).replace('[', '').replace(']', '').replace('\'', '')

b = client.session_obj['mmc-khko'].update_function_configuration(
    FunctionName='khko-lambda-test',
    Environment={
        'Variables':
                     {
                         'past_menu': sr_menu,
                         'slack_url': p_menu['slack_url']
                     }
    },
    )['Environment']['Variables']


def lunch():
    url = slack_url
    headers = {'Content-Type': 'application/json'}
    data = {
        "type" : "mrkdwn",
        "text": "선택 가능한 메뉴는 [ " + str(menu).replace("[", "").replace("]", "").replace("'", "") + " ] 입니다."
                "\n"
                "제외된 메뉴는 [ " + str(past_menu).replace("[", "").replace("]", "").replace("'", "\"") + " ] 입니다."
                "\n"
                "오늘 메뉴는 *" + today_menu + "* 입니다.\n"
                ,
        "icon_emoji": ":robot_face:"
    }
    requests.post(url=url, headers=headers, json=data)
lunch()

#def lambda_handler(event, context):
#    lunch()