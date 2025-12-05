import os
from datetime import timedelta
from dotenv import load_dotenv

# Load .env only for local development
load_dotenv()

class Config:
    # Use Railway PostgreSQL if available, else fallback to local SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_secret_key")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    PROPAGATE_EXCEPTIONS = True
