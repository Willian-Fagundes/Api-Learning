import os
from flask_migrate import Migrate
from flask import Flask
from flask_jwt_extended import JWTManager
from src.Models.base import db
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY = "chave-padrao-muito-longa-com-mais-de-32-caracteres", 
                            SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db", 
                            JWT_SECRET_KEY = "super-secretchave-padrao-muito-longa-com-mais-de-32-caracteres",
                            JWT_VERIFY_SUB = False)

    if test_config is None:
        app.config.from_pyfile("config.py", silent = True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    db.init_app(app)
    migrate.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    from src.Controllers import user, auth, role, post
    from flask import json
    from werkzeug.exceptions import HTTPException

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps({"code":e.code,"name":e.name,"description":e.description})
        response.content_type = "application/json"
        return response
    
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)
    app.register_blueprint(post.app)

    return app
