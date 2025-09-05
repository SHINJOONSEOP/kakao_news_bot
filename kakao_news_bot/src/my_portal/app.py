from flask import Flask, render_template, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import my_portal.News_DB as News_DB

app = Flask(__name__)

# 실행 로그 저장용
run_logs = []

# 뉴스 수집 함수 (예시)
def main_task():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # TODO: 여기서 뉴스 크롤링 + DB 저장 + 카톡 전송 로직 연결
    run_logs.append(f"[{now}] main_task 실행됨")
    print(run_logs[-1])

# APScheduler 백그라운드 실행
scheduler = BackgroundScheduler()
scheduler.add_job(main_task, 'interval', minutes=10)
scheduler.start()

@app.route("/")
def index():
    news = News_DB.get_all_news(limit=10)
    return render_template("index.html", news=news, logs=run_logs[-20:])

@app.route("/run-now")
def run_now():
    main_task()
    return redirect(url_for("index"))

if __name__ == "__main__":
    News_DB.init_db()
    app.run(debug=True, port=5000)
