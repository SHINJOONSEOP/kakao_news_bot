# test_news_db.py
import my_portal.News_DB as News_DB

# DB 초기화
News_DB.init_db()

'''
# 뉴스 저장 예시
News_DB.save_news(
    title="비너스 프로토콜 피싱 공격으로 2700만 달러 피해",
    url="https://www.blockmedia.co.kr/archives/970207"
)
'''


# 저장된 뉴스 조회
for row in News_DB.get_all_news():
    print(row)

