import requests
import json

# Google Chat Webhook URL
#webhook_url = {}
webhook_url = {
    "TEST" : "test"
}


# 전송할 메시지
#message = {
#    "text": "오후 6시에 DEV 환경의 서버와 DB가 종료됩니다. \n"
#            "종료 30분 전이므로 작업하고 계신 내용들 저장 부탁드리겠습니다."
#}

message = {
    "text": "TEST HOOK 연동 메시지입니다."
}

# Google Chat에 메시지 보내기
for send_url in webhook_url.values():
    response = requests.post(send_url, json=message, headers={'Content-Type': 'application/json; chartset=UTF-8'} )
#    print(send_url)

    # 결과 확인
    if response.status_code == 200:
        print('메시지가 성공적으로 발송 되었습니다.')
    else:
        print(f'메시지 발송이 실패하였습니다.: {response.status_code}, {response.text}')
