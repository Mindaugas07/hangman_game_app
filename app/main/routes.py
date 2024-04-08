from flask import render_template
from app.main import bp
from flask_login import (
    LoginManager,
    current_user,
    logout_user,
    login_user,
    login_required,
)
from app.models.user_auth.user_auth import GameUser


@bp.route("/home")
def home():
    users = GameUser.query.all()
    return render_template("user_auth/index.html", users=users)
