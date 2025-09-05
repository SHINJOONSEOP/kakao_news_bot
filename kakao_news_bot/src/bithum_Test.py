# bithum.py
import requests
#from Selenium_Test import send_message_to_chatroom  # 카톡 전송 함수 불러오기

import datetime

def bithum_airdrop_notices():
    today = datetime.datetime.now()

    # API 요청
    url = "https://api.bithumb.com/v1/notices?count=20"
    headers = {"accept": "application/json"}

    # 데이터 추출
    response = requests.get(url, headers=headers)
    data = response.json()

    # data가 리스트인지 dict인지 확인
    if isinstance(data, dict):
        notices = data.get("data", [])
    elif isinstance(data, list):
        notices = data
    else:
        notices = []

    #print(notices) 

    # 보낼 메시지를 누적
    messages = []
    for notice in notices:
        published_at_date = datetime.datetime.strptime(notice["published_at"], "%Y-%m-%d %H:%M:%S") # 문자열을 datetime 객체로 변환
        if "에어드랍" in notice["title"] and "이벤트" in notice["categories"] and published_at_date > today - datetime.timedelta(days=3):
            msg = (
                "[빗썸 에어드랍 정보]\n"
                f"제목: {notice['title']}\n"
                f"URL: {notice['pc_url']}\n"
                f"게시시간: {notice['published_at']}\n"
                +"게시일로부터 3일까지 에어드랍 정보를 공유드립니다.\n"
            )
            messages.append(msg)

    final_text = "\n\n".join(messages)

    return final_text


'''
# 카카오톡으로 전송 (메시지가 있으면)
if messages:
    final_text = "\n\n".join(messages)
    #print(final_text)
    send_message_to_chatroom("신준섭", final_text)  # 원하는 방 이름으로 바꾸기
    print("[OK] 카톡 전송 완료")
else:
    print("[INFO] 전송할 에어드랍 이벤트가 없습니다.")
'''