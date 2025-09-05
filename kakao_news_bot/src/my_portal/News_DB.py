# news_db.py
import sqlite3

DB_FILE = "news.db"

def init_db():
    """DB 초기화 (테이블 없으면 생성)"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def save_news(title: str, url: str):
    """뉴스 1건 저장 (중복 url은 무시)"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT OR IGNORE INTO news (title, url)
            VALUES (?, ?)
        """, (title, url))
        conn.commit()
    except Exception as e:
        print("DB 저장 오류:", e)
    finally:
        conn.close()

def get_all_news(limit: int = 10):
    """저장된 뉴스 가져오기"""
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, url
        FROM news
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows
