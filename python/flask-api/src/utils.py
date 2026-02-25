from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from src.app import User, db
from functools import wraps

def requires_roles(role_name):
    def decorator(f):
        @wraps(f)
        def wraped(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.get_or_404(User, user_id)
            if user.role.name != role_name:
                return {"msg": "Not Allowed"}, 403
            return f(*args, **kwargs)
        return wraped
    return decorator
