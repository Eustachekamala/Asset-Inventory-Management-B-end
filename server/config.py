import os

class Config:
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.environ.get('DATABASE_USER')}:{os.environ.get('DATABASE_PASSWORD')}@localhost/{os.environ.get('DATABASE_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback_secret_key'