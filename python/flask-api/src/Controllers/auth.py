from flask import Flask, jsonify, request, Blueprint
from src.Models.base import db
from src.Models.user import User
from src.app import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Blueprint("auth", __name__, url_prefix="/auth")

def _check_password(pw_hash, password):
    return bcrypt.check_password_hash(pw_hash, password)
    

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if not user or not _check_password(user.password, password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return {"access_token":access_token}