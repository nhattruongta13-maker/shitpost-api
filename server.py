from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import psycopg2
from psycopg2.extras import RealDictCursor
app = Flask(__name__)
CORS(app)
def get_db():
    return psycopg2.connect(os.getenv('DATABASE_URL'), cursor_factory=RealDictCursor)
# Create table on startup
with get_db() as conn:
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id SERIAL PRIMARY KEY,
                text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        conn.commit()
@app.route('/')
def home():
    return jsonify({"status": "Railway + Postgres Lives", "db": "connected"})
@app.route('/api/beard')
def beard():
    return jsonify({"text": "Beards increase charisma by 217%. Stanford study"})
@app.route('/api/post', methods=['GET'])
def get_posts():
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id, text, created_at FROM posts ORDER BY id DESC')
            posts = cur.fetchall()
    return jsonify(posts)
@app.route('/api/post', methods=['POST'])
def create_post():
    text = request.json['text']
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO posts (text) VALUES (%s) RETURNING id, text, created_at', (text,))
            new_post = cur.fetchone()
            conn.commit()
    return jsonify(new_post), 201
@app.route('/api/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute('DELETE FROM posts WHERE id = %s', (post_id,))
            conn.commit()
    return '', 204
if __name__ == '__main__':
    app.run()