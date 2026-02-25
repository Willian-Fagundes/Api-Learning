import os
import click
import sqlalchemy as sa
from flask_migrate import Migrate
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from datetime import datetime
from flask_jwt_extended import JWTManager



class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
migrate = Migrate()
jwt = JWTManager()


class Role(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    name : Mapped[str] = mapped_column(String, nullable= False)
    user : Mapped[list["User"]] = relationship(back_populates = "role")
    
    def __repr__(self) -> str:
        return f"Role(id = {self.id!r}, name = {self.name!r})"

class User(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    username : Mapped[str] = mapped_column(String, nullable = False, unique = True)
    password : Mapped[str] = mapped_column(String, nullable = False)
    role_id : Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role : Mapped["Role"] = relationship(back_populates = "user")

    def __repr__(self) -> str:
        return f"User(id = {self.id!r}, username = {self.username!r})"
        
class Post(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String, nullable=False)
    body : Mapped[str] = mapped_column(String, nullable=False)
    author_id : Mapped[int] = mapped_column(sa.ForeignKey("user.id")) 
    created : Mapped[datetime] = mapped_column(sa.DateTime, server_default= sa.func.now())
    def __repr__(self) -> str:
        return f"User(id = {self.id!r}, title = {self.title!r}, author_id{self.author_id!r})"
    
@click.command("init-db")
def init_db_command():
    global db
    with current_app.app_context():
        db.create_all()
    click.echo("db pronto")

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
    
    app.cli.add_command(init_db_command)
    db.init_app(app)
    migrate.init_app(app)
    jwt.init_app(app)

    from src.Controllers import user, auth, role, post

    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)
    app.register_blueprint(post.app)

    return app
