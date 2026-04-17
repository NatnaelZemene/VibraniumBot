import sqlite3
import logging

logger = logging.getLogger(__name__)

DB_FILE = "leaderboard.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                score INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

def add_score(user_id, username, points=1):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (user_id, username, score)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
            username=excluded.username,
            score=score + excluded.score
        ''', (user_id, username, points))
        conn.commit()

def get_top_users(limit=3):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT username, score FROM users
            ORDER BY score DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

def reset_weekly_scores():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET score = 0')
        conn.commit()