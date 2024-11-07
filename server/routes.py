from flask import Blueprint, jsonify
from models import User

routes_bp = Blueprint('routes', _name_)

@routes_bp.route('/', methods=['GET'])
def get_api():
    return jsonify({'message': 'Welcome to the API!'})

@routes_bp.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize for user in users])

@routes_bp.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify(user.serialize)