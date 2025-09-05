# bithum.py
import requests
from Selenium_Test import send_message_to_chatroom  # 카톡 전송 함수 불러오기

url = "https://api.bithumb.com/v1/notices?count=20"
headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)
data = response.json()

# data가 리스트인지 dict인지 확인
if isinstance(data, dict):
    notices = data.get("data", [])
elif isinstance(data, list):
    notices = data
else:
    notices = []

# 보낼 메시지를 누적
messages = []
for notice in notices:
    if "에어드랍" in notice["title"] and "이벤트" in notice["categories"]:
        msg = (
            f"카테고리: {', '.join(notice['categories'])}\n"
            f"제목: {notice['title']}\n"
            f"URL: {notice['pc_url']}\n"
            f"게시시간: {notice['published_at']}\n"
            f"수정시간: {notice['modified_at']}\n"
            + "-" * 30
        )
        messages.append(msg)

# 카카오톡으로 전송 (메시지가 있으면)
if messages:
    final_text = "\n\n".join(messages)
    print(final_text)
    send_message_to_chatroom("신준섭", final_text)  # 원하는 방 이름으로 바꾸기
    print("[OK] 카톡 전송 완료")
else:
    print("[INFO] 전송할 에어드랍 이벤트가 없습니다.")
