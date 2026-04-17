import os
import logging
import psycopg2

logger = logging.getLogger(__name__)

def get_connection():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        logger.error("DATABASE_URL is not set in environment variables.")
        return None
    try:
        return psycopg2.connect(db_url)
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        return None

def init_db():
    conn = get_connection()
    if not conn: return
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id BIGINT PRIMARY KEY,
                        username TEXT,
                        score INTEGER DEFAULT 0
                    )
                ''')
    finally:
        conn.close()

def add_score(user_id, username, points=1):
    conn = get_connection()
    if not conn: return
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO users (user_id, username, score)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_id) DO UPDATE SET
                    username = EXCLUDED.username,
                    score = users.score + EXCLUDED.score
                ''', (user_id, username, points))
    finally:
        conn.close()

def get_top_users(limit=3):
    conn = get_connection()
    if not conn: return []
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute('''
                    SELECT username, score FROM users
                    ORDER BY score DESC
                    LIMIT %s
                ''', (limit,))
                return cursor.fetchall()
    finally:
        conn.close()

def reset_weekly_scores():
    conn = get_connection()
    if not conn: return
    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute('UPDATE users SET score = 0')
    finally:
        conn.close()