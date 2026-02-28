from flask import Blueprint, request, jsonify
from src.Models.user import User
from src.Models.base import db
from src.app import bcrypt
from src.Views.user import UserSchema, CreateSchema
from src.utils import requires_roles
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from marshmallow import ValidationError

app = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    user_schema = CreateSchema()
    try:
        data = user_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    user = User(username = data["username"],
                password = bcrypt.generate_password_hash(data["password"]),
                role_id = data["role_id"])
    db.session.add(user)
    db.session.commit()
    return {"message" : "user created"}, HTTPStatus.CREATED

@jwt_required()
@requires_roles("admin")
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    users_schema = UserSchema(many = True)
    return users_schema.dump(users)
    
@app.route("/", methods = ["GET", "POST"])

def handle_user():
    
    if request.method == "POST":
        return _create_user()
        
    else:
        return {"user" : _list_users()}

@app.route("/<int:user_id>")
def get_user_id(user_id):
    user = db.get_or_404(User, user_id)
    return {"id" : user.id,
            "username" : user.username,
    }

@app.route("/<int:user_id>", methods = ["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    if "username" in data:
        user.username = data["username"]
        db.session.commit()
    return {"id" : user.id,
            "username" : user.username}

@app.route("/<int:user_id>", methods = ["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.delete(user)

