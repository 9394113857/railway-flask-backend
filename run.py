from app import create_app
from app.extensions import db
import os

app = create_app()

# ---------------------------------------------
# LOCAL DEVELOPMENT ONLY: Auto-create tables
# ---------------------------------------------
# Detect SQLite local environment
IS_LOCAL = "DATABASE_URL" not in os.environ

if IS_LOCAL:
    with app.app_context():
        db.create_all()
        print("✔ Local SQLite tables created.")

# ---------------------------------------------
# NORMAL FLASK RUN
# ---------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
