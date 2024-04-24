from flask import render_template, redirect, url_for, flash, request, Flask
from app.user_auth import bp
from app.extensions import db
from app.models.user_auth.user_auth import GameUser
from app.models.mongo.mongo import MongoDB
from app import game_db
import datetime
from typing import List, Dict


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


def get_todays_games(user: GameUser) -> List[Dict]:
    todays_games = []
    current_day_of_the_month = datetime.datetime.now().day
    users_played_games = game_db.find_documents(
        {
            "user email": user.email,
        },
        {"_id": 0},
    )
    for game in users_played_games:
        if game["date"].day == current_day_of_the_month:
            todays_games.append(game)
    return todays_games


@bp.route("/")
@login_required
def index():
    current_user_email = current_user.email
    user_from_db = GameUser.query.filter_by(email=current_user_email).first()

    try:
        todays_games_list = get_todays_games(user_from_db)
        return render_template(
            "index.html",
            user_from_db=user_from_db,
            todays_games_list=todays_games_list,
        )
    except:
        return render_template(
            "index.html", user=user_from_db, todays_games_list=todays_games_list
        )


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


def todays_games_statistics(user: GameUser) -> Dict:
    game_stats_dict = {}
    game_wins = game_db.query_equal("game result", "won", {"_id": 0})
    game_looses = game_db.query_equal("game result", "lost", {"_id": 0})
    wins_by_user = 0
    bad_guesses = 0
    looses_by_user = 0
    for game in game_wins:
        if (
            game["username"] == user.name
            and game["date"].day == datetime.datetime.now().day
        ):
            wins_by_user += 1
            bad_guesses += game["guesses made"]

    for game in game_looses:
        if (
            game["username"] == user.name
            and game["date"].day == datetime.datetime.now().day
        ):
            looses_by_user += 1
            bad_guesses += 6

    game_stats_dict[user.name] = {
        "wins": wins_by_user,
        "losses": looses_by_user,
        "today guesses": bad_guesses,
        "todays games": wins_by_user + looses_by_user,
    }
    return game_stats_dict


@bp.route("/<app_user>")
def user_page(app_user):

    try:
        user_from_db = GameUser.query.filter_by(name=app_user).first()
        users_played_games = game_db.find_documents(
            {"user email": user_from_db.email}, {"_id": 0}
        )
        game_stats = todays_games_statistics(user=user_from_db)

        return render_template(
            "user_auth/user_page.html",
            user_from_db=user_from_db,
            games_data=users_played_games,
            game_stats=game_stats,
        )
    except:
        print(f"User with username '{app_user}' doesn't exist!")
        return render_template(
            "user_auth/user_page.html",
            not_existing_user=app_user,
        )
