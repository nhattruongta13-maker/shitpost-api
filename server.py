from flask import Flask, jsonify, request
from flask_cors import CORS
from db import db  # <-- Import our new db module
import os
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps


app = Flask(__name__)
CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL').replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_size': 5,
    'max_overflow': 10,
    'pool_timeout': 30
}
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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
        "msg": "User created"
    }), 201

@app.post('/login')
def login():
    data = request.get_json()
    email = data.get('email')
    passwd = data.get('password')
    if not data or not email or not passwd:
        return {"error": "email and passwd required!"}, 400
    
    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, passwd):
        return {"error": "Invalid credentials"}, 401
    
    token = jwt.encode({
        'user_id': user.id,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(hours=24)
    }, app.config['SECRET_KEY'], algorithm='HS256')

    return {"token": token}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ','')

        if not token:
            return {"error": "Token missing"}
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user_id = data.get('id')
        except jwt.ExpiredSignatureError:
            return {"error": "Token expired. Login again"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Token invalid"}, 401
        
        return f(*args, **kwargs)
    return decorated

@app.post('/predict')
@token_required
def predict():
    data = request.get_json()
    prompt = "data.get('prompt')"
    if not data or not prompt:
        return {"error": "Prompt required"}, 400
    
    result = f"Echo: {prompt}"

    return {"result": result,
            "user_id": data.get('id')}

    

if __name__ == '_main_':
    app.run()