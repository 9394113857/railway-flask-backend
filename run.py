from app import create_app
from app.extensions import db
import os

# Create the Flask application
app = create_app()

# Detect if local (SQLite) or Railway (PostgreSQL)
IS_LOCAL = os.getenv("DATABASE_URL") is None

if IS_LOCAL:
    # Auto-create SQLite tables on local machine
    with app.app_context():
        db.create_all()
        print("✔ Local SQLite tables created automatically.")
else:
    print("✔ Running in PRODUCTION mode (Railway/PostgreSQL).")

# Local run only
if __name__ == "__main__":
    app.run()
