from flask import Blueprint, request, jsonify
from src.Models.base import db
from src.Models.post import Post
from src.utils import requires_roles
from src.Views.post import CreateSchema, PostSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from marshmallow import ValidationError

app = Blueprint("post", __name__, url_prefix="/posts")


def _create_post():
    post_schema = PostSchema()
    try:
        data = post_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    author_id = get_jwt_identity()
    post = Post(title = data["title"],
                body = data["body"],
                author_id = author_id,
                )
    db.session.add(post)
    db.session.commit()
    return {"message" : "user created"}, HTTPStatus.CREATED
    

@jwt_required()
@requires_roles("admin")
def _list_posts():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    return [{"id" : post.id,
             "title" : post.title,
             "body": post.body,
             "author_id" : post.author_id} for post in posts]

@app.route("/", methods = ["GET", "POST"])
def handle_post():
    if request.method == "POST":
        _create_post()
        return {"message" : "post created"}, HTTPStatus.CREATED
    else:
        return {"post" : _list_posts()}
    
@app.route("/<int:post_id>")
def get_post_id(post_id):
    post = db.get_or_404(Post, post_id)
    return {"id" : post.id,
            "title" : post.title,
            "body" : post.body,
            "created" : post.created,
            "author_id" : post.author_id
    }

@app.route("/<int:post_id>", methods = ["PATCH"])
def update_post_title(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json

    if "title" in data:
        post.title = data["title"]
        db.session.commit()
        return {"id" : post.id,
            "title" : post.title}
    elif "body" in data:
        post.body = data["body"]
        db.session.commit()
        return {"id" : post.id,
            "body" : post.body}
    

@app.route("/<int:post_id>", methods = ["DELETE"])
@jwt_required()
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.delete(post)