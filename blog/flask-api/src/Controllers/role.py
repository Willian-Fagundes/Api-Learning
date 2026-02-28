from flask import Blueprint, request, jsonify
from src.Models.user import User
from src.Models.role import Role
from src.Models.base import db
from flask_jwt_extended import jwt_required, get_jwt_identity

app = Blueprint("role", __name__, url_prefix="/roles")

@app.route("/", methods = ["POST"])
def create_role():
    data = request.json
    role = Role(name = data["name"])
    db.session.add(role)
    db.session.commit()
    return{"message":"Role created!"}, 201