from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
import sqlalchemy as sa

from src.models.base import db

class User(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key = True)
    username : Mapped[str] = mapped_column(String, nullable = False, unique = True)
    password : Mapped[str] = mapped_column(String, nullable = False)
    role_id : Mapped[int] = mapped_column(sa.ForeignKey("role.id"))
    role : Mapped["Role"] = relationship(back_populates = "user")

    def __repr__(self) -> str:
        return f"User(id = {self.id!r}, username = {self.username!r})"