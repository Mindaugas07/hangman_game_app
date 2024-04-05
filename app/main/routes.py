from flask import render_template
from app.main import bp
from flask_login import (
    LoginManager,
    current_user,
    logout_user,
    login_user,
    login_required,
)


@bp.route("/home")
def home():
    return render_template("index.html")
