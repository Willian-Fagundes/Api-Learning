from flask import Blueprint, request
from src.views.user import UserSchema, CreateSchema
from src.models.user import User
from src.models.base import db
from http import HTTPStatus
from marshmallow import ValidationError


app = Blueprint("user", __name__, url_prefix = "/users")

def _create_user():
    user_schema = CreateSchema()
    try:
        data = user_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    user = User(username = data["username"],
                password = data["password"])
    db.session.add(user)
    db.session.commit()
    return {"message" : "user created"}, HTTPStatus.CREATED

@app.route("/")
def create_user(methods = ["POST"]):
    return _create_user()
    
