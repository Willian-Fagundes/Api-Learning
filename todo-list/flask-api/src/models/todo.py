from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from datetime import datetime
import sqlalchemy as sa
from src.models.base import db

class Todo(db.Model):

    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String, nullable=False)
    chore : Mapped[str] = mapped_column(String, nullable=False)
    author_id : Mapped[int] = mapped_column(sa.ForeignKey("user.id")) 
    created : Mapped[datetime] = mapped_column(sa.DateTime, server_default= sa.func.now())

    def __repr__(self) -> str:
        return f"User(id = {self.id!r}, title = {self.title!r}, author_id{self.author_id!r})"
    