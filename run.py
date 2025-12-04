from app import create_app
from app.extensions import db
import os

app = create_app()

# --------------------------------------------------
# LOCAL DEVELOPMENT (SQLite auto create tables)
# --------------------------------------------------
# Railway sets DATABASE_URL → so IS_LOCAL = False
IS_LOCAL = os.getenv("DATABASE_URL") is None

if IS_LOCAL:
    with app.app_context():
        db.create_all()
        print("✔ Local SQLite tables created automatically.")
else:
    print("✔ Running in PRODUCTION mode (Railway/PostgreSQL).")

# --------------------------------------------------
# NORMAL FLASK RUN (local only)
# --------------------------------------------------
if __name__ == "__main__":
    app.run()
