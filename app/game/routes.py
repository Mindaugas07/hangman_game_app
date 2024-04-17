from flask import render_template, request, url_for, redirect, Flask
from app.game import bp
from app.extensions import db
from app.models.game.game import HangmanGame
from flask_login import login_required, current_user
import string
from app import game_db
from datetime import datetime
from typing import Dict

app = Flask(__name__)


def game_data_blueprint(
    current_username: str,
    current_username_email: str,
    current_date: datetime,
    current_time: datetime,
    game_status_db: str,
    game_word: str,
) -> Dict:
    return {
        "userame": current_username,
        "user email": current_username_email,
        "date": current_date,
        "time": current_time,
        "game result": game_status_db,
        "game word": game_word,
    }


def get_game_status_data(status: str) -> Dict:
    if status == "win":
        game_status = f"""You won!!!"""
        game_status_db = "won"
    elif status == "loose":
        game_status = f"""Sorry you lost!
                The word was: '{new_game_obj.game_word}'.
                Do you want to play again?"""
        game_status_db = "lost"
    current_username = current_user.name
    current_username_email = current_user.email
    current_date = datetime.now()
    current_time = datetime.now().strftime("%H:%M:%S")
    game_word = new_game_obj.game_word
    document = game_data_blueprint(
        current_username,
        current_username_email,
        current_date,
        current_time,
        game_status_db,
        game_word,
    )
    return document


@bp.route("/game", methods=("GET", "POST"))
@login_required
def game():

    if request.method == "POST":
        global new_game_obj
        HangmanGame.BAD_GUESSES = 0
        new_game_obj = HangmanGame(current_user.name, used_letters=set())
        return redirect("start_game")
    else:
        return render_template("game/new_game.html")


@bp.route("/start_game", methods=("GET", "POST"))
@login_required
def start_game():

    guessed_letters = new_game_obj.join_guessed_letters()
    not_used_letters = list(string.ascii_lowercase)
    game_status = None

    if request.method == "POST":
        player_guess = request.form["letter"]
        new_game_obj.used_letters.add(player_guess)
        guessed_letters = new_game_obj.join_guessed_letters()
        not_used_letters = new_game_obj.not_used_letters(guessed_letters)
        if player_guess not in new_game_obj.game_word:
            HangmanGame.BAD_GUESSES += 1

    selected_word = new_game_obj.guessing_word()

    if new_game_obj.game_over():
        if "_" not in selected_word:
            document = get_game_status_data("win")
            result = game_db.collection.insert_one(document)
            print(f"Inserted document with ID: {result.inserted_id}")
            not_used_letters = []
        else:
            document = get_game_status_data("loose")
            result = game_db.collection.insert_one(document)
            print(f"Inserted document with ID: {result.inserted_id}")
            not_used_letters = []

    return render_template(
        "game/index.html",
        guessed_letters=guessed_letters,
        game_picture="/static/game_images/hangman%d.png" % HangmanGame.BAD_GUESSES,
        selected_word=selected_word,
        not_used_letters=not_used_letters,
        game_status=game_status,
    )
