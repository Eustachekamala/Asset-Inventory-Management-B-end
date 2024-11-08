from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token
from models import User 
from database import db
from flask_cors import CORS 

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
CORS(app, supports_credentials=True)
# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
    f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')  # Use a strong key

# Initialize the database and migration
db.init_app(app)  # Initialize db with the app
migrate = Migrate(app, db)
jwt = JWTManager(app)

# Define routes
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
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.serialize)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json  # Get JSON data from request
    print(f"Received login request: {data}")  # Log the request

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    print(f"User found: {user}")  # Log found user or None

    if user:
        print(f"Stored password hash: {user.password}")
        if check_password_hash(user.password, password):
            # Create access token with serializable user information
            access_token = create_access_token(identity={
                'id': user.id,
                'username': user.username,
                'role': user.role.name if user.role else None
            })
            return jsonify(access_token=access_token), 200
        else:
            return jsonify({'msg': 'Bad username or password'}), 401
    else:
        return jsonify({'msg': 'Bad username or password'}), 401
    
@app.route('/api/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    print(f"Received register request: {data}")

    # Extract data with validation
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    email = data.get('email')

    if not username or not password or not role or not email:
        return jsonify({'msg': 'Missing required fields'}), 400

    # Check if user already exists
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'msg': 'User already exists'}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user
    new_user = User(username=username, password=hashed_password, role=role, email=email)
    db.session.add(new_user)

    try:
        db.session.commit()
        print(f"User created successfully: {username}, Role: {role}") 
        return jsonify({'message': 'User created successfully', 'role': role}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error creating user: {e}")
        return jsonify({'msg': 'Failed to create user'}), 500

# Define error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# CLI command to show the database state (optional)
@app.cli.command("show_users")
def show_users():
    """Displays all users in the database."""
    with app.app_context():
        users = User.query.all()
        for user in users:
            print(user.serialize)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)