
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from Selenium_Test import send_message_to_chatroom  # 카톡 전송 함수 불러오기

from my_portal import News_DB

from bithum_Test import bithum_airdrop_notices  # 빗썸 에어드랍 함수 불러오기
import time
import random

News_DB.init_db()

chrome_options = Options()
chrome_options.add_argument("--headless")        # 브라우저 창을 띄우지 않음
chrome_options.add_argument("--disable-gpu")     # GPU 가속 비활성화 (일부 환경 필요)
chrome_options.add_argument("--no-sandbox")      # 샌드박스 비활성화 (리눅스에서 자주 씀)
chrome_options.add_argument("--disable-dev-shm-usage")  # 메모리 공유 문제 방지

def main_process():

    # 크롬 드라이버 자동 설치 및 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

    # 1) 웹페이지 열기
    driver.get("https://coinness.com/article")
    
    time.sleep(3)  # 로딩 대기

    wrapper = driver.find_element(By.CLASS_NAME, "ArticleWrapper-sc-42qvi5-0")

    new_title = wrapper.find_element(By.CSS_SELECTOR, "h3").text.strip()
    new_url = wrapper.get_attribute("href")

    #DB가공
    rows = News_DB.get_all_news(limit=20)
    news_array = [[row[1], row[2]] for row in rows]

    # DB에서 가져온 news_array와 비교
    is_duplicate = any((t == new_title and u == new_url) for t, u in news_array)

    if is_duplicate:
        print("[INFO] 이미 저장된 뉴스입니다.")
    else:
        print("[NEW] 새로운 뉴스 발견!")
        # DB 저장 및 카카오톡 전송
        News_DB.save_news(new_title, new_url)
        send_message_to_chatroom("신준섭", f"[코인니스 뉴스] \n제목 : {new_title}\n주소 : {new_url}\nbug")
    # --- 웹사이트 닫기 ---
    driver.quit()

def sub_process():
    # 크롬 드라이버 자동 설치 및 실행
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)

    # 1) 웹페이지 열기
    driver.get("https://coinness.com/news")
    time.sleep(3)  # 로딩 대기


    wrapper = driver.find_element(By.CLASS_NAME, "BreakingNewsWrap-sc-glfxh-1")
    articles = wrapper.find_element(By.CSS_SELECTOR, "div.BreakingNewsContentWrap-sc-glfxh-3.kHsPEO a")

    new_url = articles.get_attribute("href")
    new_title = articles.text.strip()


    #DB가공
    rows = News_DB.get_all_news(limit=20)
    news_array = [[row[1], row[2]] for row in rows]

    # DB에서 가져온 news_array와 비교
    is_duplicate = any((t == new_title and u == new_url) for t, u in news_array)

    if is_duplicate:
        print("[INFO] 이미 저장된 속보입니다.")
    else:
        print("[NEW] 새로운 뉴스 발견!")
        # DB 저장 및 카카오톡 전송
        News_DB.save_news(new_title, new_url)
        send_message_to_chatroom("신준섭", f"[코인니스 속보] \n제목 : {new_title}\n주소 : {new_url}\nbug")

    # --- 웹사이트 닫기 ---
    driver.quit()


if __name__ == "__main__":
    while True:
        #main_process()
        sub_process()
        notice = bithum_airdrop_notices()  # 함수 실행 결과를 저장
        if notice:  # 문자열이 비어있지 않다면
            send_message_to_chatroom("신준섭", notice)
        else:
            print("[INFO] 전송할 에어드랍 이벤트가 없습니다.")
        time.sleep(1) 
        print("=== 10분 대기 ===")
        time.sleep(60 + random.randrange(1,7))  # 61~66초 대기


