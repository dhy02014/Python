import requests
import random
import os
import boto3

client = boto3.client('lambda')

menu = ['김치찌개(그냥찌개집)', '햄버거', '중식', '돈까스(백소정)', '부대찌개(이태리부대찌개)', '칼국수(명동칼국수)', '국밥', '뼈해장국(청년감자탕)', '마제소바(멘야유메미루)', '곰탕(1974비래옥)', \
'한식뷔페(오미라)']
past_menu = os.environ['past_menu']
lp_menu = past_menu.split(', ')
if past_menu:
    for i in lp_menu:
        menu.remove(i)

today_menu = random.choice(menu)
lp_menu.pop(0)
lp_menu.append(today_menu)
if today_menu == '국밥':
    gukbap = ['시골국밥', '농민백암순대', '해안사골순댓국', '신의주찹쌀순대']
    add_location = random.choice(gukbap)
    today_menu = f"{today_menu + "(" + add_location + ")"}"
elif today_menu == '중식':
    jungsik = ['카이', '짬뽕지존', '홍콩반점0410(강남역점)']
    add_location = random.choice(jungsik)
    today_menu = f"{today_menu + "(" + add_location + ")"}"
sr_menu = str(lp_menu).replace('[', '').replace(']', '').replace('\'', '')

b = client.update_function_configuration(
    FunctionName='khko-lambda-test',
    Environment={
        'Variables':
                     {
                         'past_menu': sr_menu,
                         'slack_url': os.environ['slack_url'],
                         'test_url': os.environ['test_url']
                     }
    },
    )['Environment']['Variables']


def lunch():
    #url = os.environ['slack_url']
    url = os.environ['test_url']
    headers = {'Content-Type': 'application/json'}
    data = {
        "type" : "mrkdwn",
        "text": "선택 가능한 메뉴는 [ " + str(menu).replace("[", "").replace("]", "").replace("'", "") + " ] 입니다.\n"
                "\n"
                "최근 5일간 제외된 메뉴는 [ " + str(past_menu).replace("[", "").replace("]", "").replace("'", "\"") + " ] 입니다.\n"
                "\n"
                "오늘 메뉴는 *" + today_menu + "* 입니다.\n"
                "\n"
                "*점심식사 참여:o: 미참여:x: 여부를 이모티콘으로 표기 부탁드리겠습니다.*"
                ,
        "icon_emoji": ":robot_face:"
    }
    requests.post(url=url, headers=headers, json=data)


def lambda_handler(event, context):
    lunch()