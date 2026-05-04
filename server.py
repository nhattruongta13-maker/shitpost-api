from flask import Flask, jsonify, request
from flask_cors import CORS
from db import db  # <-- Import our new db module
import os
from werkzeug.security import generate_password_hash


app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300
}

db.init_app(app)
from models import User
with app.app_context():
    db.create_all()

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

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error":"Email and password required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error":"Email already exists"}), 400
    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        dually=0
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "msg": "User created",
        "id": user.id,
        "email":user.email,
        "duallies": user.dually
    }), 201

if __name__ == '_main_':
    app.run()