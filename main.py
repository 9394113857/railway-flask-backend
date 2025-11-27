import os
from datetime import datetime, timedelta, date
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt, get_jwt_identity, unset_jwt_cookies
)
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# -------------------------
# MODELS
# -------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(20), unique=True)
    address = db.Column(db.String(255))

class TokenBlacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36))
    created_at = db.Column(db.DateTime)

# -------------------------
# JWT Token Blocklist
# -------------------------
@jwt.token_in_blocklist_loader
def check_token(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return TokenBlacklist.query.filter_by(jti=jti).first() is not None


# -------------------------
# ROUTES
# -------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask Deta backend running!"})

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"message": "Username already taken"}), 400

    hashed_pw = generate_password_hash(data["password"])

    new_user = User(
        username=data["username"],
        password=hashed_pw,
        name=data.get("name"),
        email=data.get("email"),
        phone=data.get("phone"),
        address=data.get("address")
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token})


@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    uid = get_jwt_identity()
    user = User.query.get(uid)

    if not user:
        return jsonify({"message": "Not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "address": user.address
    })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run()
