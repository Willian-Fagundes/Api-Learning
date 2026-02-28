from src.app import ma
from src.Views.user import UserSchema
from src.Models.post import Post


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Post

    id = ma.auto_field()
    title = ma.auto_field()
    body = ma.auto_field()
    author_id = ma.Nested(UserSchema)
    created = ma.auto_field()

class CreateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        
    title = ma.auto_field()
    body = ma.auto_field()
    
    