from flask import Blueprint

bp = Blueprint("user_auth", __name__)


from app.user_auth import routes
