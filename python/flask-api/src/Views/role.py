from src.app import ma
from src.Models.role import Role

class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta():
        model = Role
    
    id = ma.auto_field()
    name = ma.auto_field()
    