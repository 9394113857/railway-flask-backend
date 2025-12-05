from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from config import Config
from app.extensions import db, jwt

# 🔥 Import all models so Flask-Migrate can detect them
from app import models

# Global migrate instance
migrate = Migrate()

# Blueprints
from app.routes.auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS for Angular requests
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)   # REQUIRED for flask db migrate/upgrade

    # Register routes
    app.register_blueprint(auth_bp, url_prefix="/api")

    return app
