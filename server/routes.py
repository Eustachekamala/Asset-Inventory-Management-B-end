from flask import jsonify
from app import app, db
from models import User

@app.route('/', methods=['GET'])
def get_api():
    return jsonify({'message': 'Welcome to the API!'})

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize for user in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.serialize)