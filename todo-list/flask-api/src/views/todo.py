from src.app import ma
from src.models.todo import Todo
from src.views.user import UserSchema


class TodoSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Todo
    
    id = ma.auto_field()
    title = ma.auto_field()
    chore = ma.auto_field()
    created = ma.auto_field()
    author_id = ma.Nested(UserSchema)


class CreateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Todo
        
    title = ma.auto_field()
    body = ma.auto_field()