
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from Selenium_Test import send_message_to_chatroom  # 카톡 전송 함수 불러오기

import time

# 크롬 드라이버 자동 설치 및 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 1) 웹페이지 열기
driver.get("https://coinness.com/article")
time.sleep(2)  # 페이지 로딩 대기
list = driver.find_elements(By.CLASS_NAME, "ArticleWrapper-sc-42qvi5-0")
time.sleep(1)  # 페이지 로딩 대기

print(f"[INFO] 총 {len(list)}개의 이벤트를 찾았습니다.")
print(list)

titles = []
urls = []

for x in list:
    # 제목
    try:
        title = x.find_element(By.CSS_SELECTOR, "a").text
    except:
        title = ""
    titles.append(title)

    # url
    try:
        url = x.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
    except:
        url = ""
    urls.append(url)

messages = ""
#messages = titles[0]
#print(messages)
# 카카오톡으로 전송 (메시지가 있으면)
if messages:
    #final_text = "\n\n".join(messages)
    #print(messages)
    send_message_to_chatroom("신준섭", messages)  # 원하는 방 이름으로 바꾸기
    print("[OK] 카톡 전송 완료")
else:
    print("[INFO] 전송할 에어드랍 이벤트가 없습니다.")
