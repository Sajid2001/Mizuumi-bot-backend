from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

def require_auth(func):
    @jwt_required()  # Requires a valid JWT for authentication
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()

        setattr(request, "user_id", user_id)

        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper