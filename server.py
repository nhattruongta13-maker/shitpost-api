from flask import Flask, jsonify, request
from flask_cors import CORS
import db  # <-- Import our new db module

app = Flask(__name__)
CORS(app)

# Run migrations once on startup
db.run_migrations()

@app.route('/')
def home():
    return jsonify({"status": "Railway + Postgres Lives", "db": "separated"})

@app.route('/api/beard')
def beard():
    return jsonify({"text": "Beards increase charisma by 217%. Stanford study"})

@app.route('/api/post', methods=['GET'])
def get_posts():
    posts = db.get_all_posts()  # <-- No SQL here
    return jsonify(posts)

@app.route('/api/post', methods=['POST'])
def create_post():
    text = request.json['text']
    new_post = db.create_post(text)  # <-- No SQL here
    return jsonify(new_post), 201

@app.route('/api/post/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    db.delete_post(post_id)  # <-- No SQL here
    return '', 204

if __name__ == '_main_':
    app.run()