from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token
from models import User, Asset, Request, RequestType, UrgencyLevel, RequestStatus 
from database import db
from flask_cors import CORS 


# Load environment variables from .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
CORS(app, supports_credentials=True)
# Configure the database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
#     f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
# )
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asset_inventory.db'

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

@app.route('/api/requests', methods=['POST'])
def request_asset():
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'No data provided'}), 400
    
    # Extract fields from the request data
    username = data.get('username')
    asset_id = data.get('asset_id')
    urgency_level = data.get('urgency_level')
    status = data.get('status')
    request_type = data.get('request_type')
    reason = data.get('reason', '')
    quantity = data.get('quantity', 1)  # Default to 1 if not provided
    
    # Validate that all required fields are provided
    if not username or not asset_id or not urgency_level or not status or not request_type:
        return jsonify({'msg': 'Invalid data provided, missing required fields'}), 400
    
    # Validate Enum values (RequestType, UrgencyLevel, RequestStatus)
    try:
        urgency_level = UrgencyLevel[urgency_level]  # This will raise a KeyError if invalid
        status = RequestStatus[status]
        request_type = RequestType[request_type]
    except KeyError:
        return jsonify({'msg': 'Invalid enum value provided'}), 400

    # Check if the user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'msg': 'User not found'}), 404
    
    # Check if the asset exists
    asset = Asset.query.filter_by(id=asset_id).first()  # Correct query by asset id
    if not asset:
        return jsonify({'msg': 'Asset not found'}), 404
    
    # Create the new request object
    new_request = Request(
        user_id=user.id,
        asset_id=asset.id,
        request_type=request_type,  # Set the request type (New_Asset or Repair)
        reason=reason,  # Optional field, defaults to empty string
        quantity=quantity,  # Optional field, defaults to 1
        urgency=urgency_level,  # Urgency level (Low, Medium, High)
        status=status  # Status (Pending, Approved, Rejected)
    )
    
    # Add the new request to the session and commit to the database
    db.session.add(new_request)
    db.session.commit()

    return jsonify({'msg': 'Request created successfully', 'request_id': new_request.id}), 201

@app.route('/api/requests', methods=['GET'])
def get_requests():
    try:
        # Fetch all requests from the database
        requests = Request.query.all()
        
        # Serialize the requests and send them as JSON response
        serialized_requests = [request.serialize for request in requests]
        
        return jsonify(serialized_requests), 200  # OK status
        
    except Exception as e:
        # Return a detailed error message if something goes wrong
        print(f"Error occurred: {e}")  # Log error for debugging purposes
        return jsonify({'msg': 'Internal server error', 'error': str(e)}), 500

@app.route('/api/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    data = request.get_json()
    if not data:
        return jsonify({'msg': 'No data provided'}), 400
    
    # Extract fields from the request data
    request_type = data.get('request_type')
    reason = data.get('reason', '')
    quantity = data.get('quantity', 1)  # Default to 1 if not provided
    
    # Validate that all required fields are provided
    if not request_type or not reason or not quantity:
        return jsonify({'msg': 'Invalid data provided, missing required fields'}), 400
    
    # Validate Enum values (RequestType, UrgencyLevel, RequestStatus)
    try:
        request_type = RequestType[request_type]
    except KeyError:
        return jsonify({'msg': 'Invalid enum value provided'}), 400
    
    # Check if the request exists
    request = Request.query.get(request_id)
    if not request:
        return jsonify({'msg': 'Request not found'}), 404
    
    # Update the request
    request.request_type = request_type
    request.reason = reason
    request.quantity = quantity
    
    # Commit the changes to the database
    db.session.commit()
    
    return jsonify({'msg': 'Request updated successfully'}), 200

@app.route('/api/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    request = Request.query.get(request_id)
    if not request:
        return jsonify({'msg': 'Request not found'}), 404
    
    # Delete the request
    db.session.delete(request)
    
    # Commit the changes to the database
    db.session.commit()
    
    return jsonify({'msg': 'Request deleted successfully'}), 200
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

