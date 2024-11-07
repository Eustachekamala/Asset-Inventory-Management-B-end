from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from config import Config

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy and Migrate globally
db = SQLAlchemy()
migrate = Migrate()

# Create the Flask application factory
def create_app():
    # Create an instance of the Flask application
    app = Flask(__name__)
    
    # Load the app's configuration
    app.config.from_object(Config)
    
    # Initialize the extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import routes after app is created
    from routes import routes_bp  # Assuming 'routes_bp' is your Blueprint name

    # Register the blueprint
    app.register_blueprint(routes_bp)  # Register the routes blueprint

    return app
