from flask import render_template, redirect, url_for, flash, request, Flask, abort
from app.user_auth import bp
from app.extensions import db
from app.models.user_auth.user_auth import GameUser
from app.mongo.mongo import MongoDB
from app import game_db
import datetime
from typing import List, Dict
from app.helper_functions.helper_functions import (
    get_todays_games,
    todays_games_statistics,
    get_user_all_time_statistics,
    all_games_statistics_dict,
)


from app.logging.logging_config import dictConfig

from playsound import playsound
from tkinter import *


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


@bp.route("/500")
def error500():
    abort(500)


@bp.route("/<bad_url>")
def error404(bad_url):
    abort(404)


@bp.errorhandler(404)
@login_required
def page_not_found(error):
    return render_template("errors/404.html"), 404


@bp.errorhandler(500)
def internal_error(error):
    return render_template("errors/500.html"), 500


@bp.route("/")
@login_required
def index():
    try:
        current_user_email = current_user.email
        user_from_db = GameUser.query.filter_by(email=current_user_email).first()
        todays_games_list = get_todays_games(user_from_db)[:10]

        return render_template(
            "index.html",
            user=user_from_db,
            todays_games_list=todays_games_list,
        )
    except Exception as exception:
        app.logger.error(
            f" error: {exception} was received while today's user's data did not load in route user_auth.index! "
        )
        return render_template("index.html")


from app.forms import forms


@bp.route("/register", methods=["GET", "POST"])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for("user_auth.index"))
    form = forms.RegistrationForm()
    email = form.email.data
    username = form.name.data
    user_by_username = GameUser.query.filter_by(name=username).first()
    user_by_email = GameUser.query.filter_by(email=email).first()
    if user_by_email:
        flash("Email address already exist.", "danger")
        return redirect(url_for("user_auth.register"))
    elif user_by_username:
        flash("Username already exist.", "danger")
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


@bp.route("/profile/<app_user>")
def user_page(app_user):
    try:
        user_from_db = GameUser.query.filter_by(name=app_user).first()
        users_all_played_games_stats = get_user_all_time_statistics(user_from_db)
        todays_game_stats = todays_games_statistics(user=user_from_db)
        user_all_time_stat = all_games_statistics_dict([user_from_db])

        return render_template(
            "user_auth/user_page.html",
            user_from_db=user_from_db,
            games_data=users_all_played_games_stats[:10],
            game_stats=todays_game_stats,
            user_all_time_stat=user_all_time_stat,
        )
    except Exception as exception:
        app.logger.error(
            f" error: {exception} was received while non exsistant user's '{app_user}' profile data did not load in route 'user_auth.user_page'! "
        )
        return render_template(
            "user_auth/user_page.html",
            not_existing_user=app_user,
        )
