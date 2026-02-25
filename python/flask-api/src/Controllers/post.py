from flask import Blueprint, request, jsonify
from src.app import db, Post
from src.utils import requires_roles
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus

app = Blueprint("post", __name__, url_prefix="/posts")

#def _create_post():
#    data = request.json
#    post = Post(title = data["title"],
#                body = data["body"],
#                author_id = data["author_id"],
#                created = data["created"])
#    db.session.add(post)
#    db.session.commit()


@app.route("/", methods = ["GET", "POST"])
def handle_post():
    if request.method == "POST":
        #_create_post()
        return {"message" : "post created"}, HTTPStatus.CREATED
    else:
        return {"post" : []}