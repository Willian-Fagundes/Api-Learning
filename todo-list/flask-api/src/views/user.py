from src.app import ma
from src.views.role import RoleSchema
from src.models.user import User


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    role = ma.Nested(RoleSchema)

class CreateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    
    username = ma.auto_field()
    password = ma.auto_field()
    role_id = ma.auto_field()