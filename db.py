"""
数据库模块 - 记录已推送文章，避免重复
"""

import sqlite3
import os
from datetime import date
from config import DB_PATH


def _ensure_dir():
    """确保数据库目录存在"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def init_db():
    """初始化数据库"""
    _ensure_dir()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pushed_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_hash TEXT UNIQUE NOT NULL,
            title TEXT,
            domain TEXT,
            pushed_date TEXT NOT NULL,
            source TEXT
        )
    """)
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_url_hash ON pushed_articles(url_hash)
    """)
    conn.commit()
    conn.close()


def is_pushed(url_hash: str) -> bool:
    """检查某篇文章是否已经推送过"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pushed_articles WHERE url_hash = ?", (url_hash,))
    result = cur.fetchone()
    conn.close()
    return result is not None


def mark_pushed(url_hash: str, title: str, domain: str, source: str):
    """标记一篇文章为已推送"""
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO pushed_articles (url_hash, title, domain, pushed_date, source) VALUES (?, ?, ?, ?, ?)",
            (url_hash, title, domain, today, source),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # 已经存在，忽略
    finally:
        conn.close()


def get_stats() -> dict:
    """获取推送统计信息"""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM pushed_articles")
    total = cur.fetchone()[0]
    cur.execute(
        "SELECT domain, COUNT(*) FROM pushed_articles GROUP BY domain ORDER BY COUNT(*) DESC"
    )
    by_domain = dict(cur.fetchall())
    conn.close()
    return {"total": total, "by_domain": by_domain}