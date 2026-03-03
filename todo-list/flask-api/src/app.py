import os
from flask import Flask, Blueprint
from src.models.base import db, Base
from src.models.user import User
from src.models.role import Role
from src.models.todo import Todo
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config = False)
    app.config.from_mapping(SECRET_KEY = "chave-padrao", 
                            SQLALCHEMY_DATABASE_URI = "sqlite:///todo1.db", 
                            JWT_SECRET_KEY = "super-secretchave-padrao",
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
    with app.app_context():
        db.create_all()
    
    return app
    
