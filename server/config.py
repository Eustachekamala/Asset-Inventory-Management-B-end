import os

class Config:
    DATABASE_USER = os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
    DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')       
    DATABASE_NAME = os.environ.get('DATABASE_NAME')

    if not DATABASE_USER:
        print("DATABASE_USER is not set")
    if not DATABASE_PASSWORD:
        print("DATABASE_PASSWORD is not set")
    if not DATABASE_NAME:
        print("DATABASE_NAME is not set")

    if not all([DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME]):
        raise ValueError("Missing required environment variables for database configuration.")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}?sslmode=require"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback_secret_key'

# For debugging: print the environment variable values
print("DATABASE_USER:", Config.DATABASE_USER)
print("DATABASE_PASSWORD:", Config.DATABASE_PASSWORD)
print("DATABASE_HOST:", Config.DATABASE_HOST)
print("DATABASE_PORT:", Config.DATABASE_PORT)
print("DATABASE_NAME:", Config.DATABASE_NAME)
print("SECRET_KEY:", Config.SECRET_KEY)