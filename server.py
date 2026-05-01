from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

posts =[]

@app.route('/api/beard')
def get_fact():
    beard_fact = "Beards increase charisma by 217%. Stanford study"
    return jsonify({"text" : beard_fact})

@app.route('/api/post', methods=['POST'])
def create_post():
    data = request.get_json()
    user_text = data.get('content')
    posts.append(user_text)
    return jsonify({"message" : "Flask got your post",
                    "you_sent" : user_text})

@app.route('/api/post/<int:index>', methods=['DELETE'])
def delete_post(index):
    if 0 <= index < len(posts):
        posts.pop(index)
        return jsonify({"status":"deleted", "index":index})
    return jsonify({"status":"Error, dumbass"}), 400

@app.route('/api/post')
def get_post():
    return jsonify(posts)



if __name__ == '__main__':
    app.run(port=5000, debug=True)