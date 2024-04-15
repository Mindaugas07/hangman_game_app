from flask import render_template, redirect, url_for, flash, request, Flask
from app.user_auth import bp
from app.extensions import db
from app.models.user_auth.user_auth import GameUser
from app.models.mongo.mongo import MongoDB
from app import game_db

from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import (
    LoginManager,
    current_user,
    logout_user,
    login_user,
    login_required,
)


app = Flask(__name__)

bcrypt = Bcrypt(app)
mail = Mail(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    db.create_all()
    return GameUser.query.get(int(user_id))


@bp.route("/")
@login_required
def index():
    users = GameUser.query.all()
    return render_template("user_auth/index.html", users=users)


from app.forms import forms


@bp.route("/register", methods=["GET", "POST"])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for("user_auth.index"))
    form = forms.RegistrationForm()
    email = form.email.data
    user = GameUser.query.filter_by(email=email).first()
    if user:
        flash("Email address already exists.", "danger")
        return redirect(url_for("user_auth.register"))
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = GameUser(
            name=form.name.data,
            email=form.email.data,
            password=encrypted_password,
        )
        db.session.add(user)
        db.session.commit()
        flash("You successfully registered!", "succes")
        return redirect(url_for("user_auth.index"))
    return render_template("user_auth/register.html", title="Register", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user_auth.index"))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = GameUser.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return (
                redirect(next_page)
                if next_page
                else redirect(url_for("user_auth.index"))
            )
        else:
            flash("Login was unsuccessfull. Check e-mail and password.", "danger")
    return render_template("user_auth/login.html", title="Login", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@bp.route("/<app_user>")
def user_page(app_user):
    try:
        user_from_db = GameUser.query.filter_by(name=app_user).first()

        print(user_from_db.name)
        user_email = str(user_from_db.email)
        print(user_email)
        users_played_games = game_db.find_documents(
            {"user email": user_from_db.email}, {"_id": 0}
        )
        print(users_played_games)

    except:
        print(f"No player exists with username '{app_user}'!")
    return render_template(
        "user_auth/user_page.html",
        user_name=user_from_db,
        not_existing_user=app_user,
        games_data=users_played_games,
    )
