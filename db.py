import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    """Get a fresh connection to Postgres"""
    return psycopg2.connect(
        os.getenv('DATABASE_URL'), 
        cursor_factory=RealDictCursor
    )

def run_migrations():
    """Run all .sql files in migrations/ folder on startup"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Read and execute our SQL file
            with open('migrations/001_init.sql', 'r') as f:
                cur.execute(f.read())
            conn.commit()
    print("✅ Migrations complete: tables ready")

def get_all_posts():
    """SELECT * FROM posts"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, text, created_at FROM posts ORDER BY id DESC')
            return cur.fetchall()

def create_post(text):
    """INSERT INTO posts"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO posts (text) VALUES (%s) RETURNING id, text, created_at', 
                (text,)
            )
            new_post = cur.fetchone()
            conn.commit()
            return new_post

def delete_post(post_id):
    """DELETE FROM posts"""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM posts WHERE id = %s', (post_id,))
            conn.commit()