from flask import render_template, request, url_for, redirect, Flask
from app.game import bp
from app.extensions import db
from app.models.game.game import HangmanGame
from app.models.user_auth.user_auth import GameUser
from flask_login import login_required, current_user
import string
from app import game_db
from datetime import datetime
from typing import Dict

app = Flask(__name__)

# serialized game status
def get_game_status_data(status: str, guesses_made: int) -> Dict:
    """Status must be 'won' or 'lost'"""
    game_status_db = status
    current_username = current_user.name
    current_username_email = current_user.email
    current_date = datetime.now()
    current_time = datetime.now().strftime("%H:%M:%S")
    game_word = new_game_obj.game_word
    return {
        "username": current_username,
        "user email": current_username_email,
        "date": current_date,
        "time": current_time,
        "game result": game_status_db,
        "game word": game_word,
        "guesses made": guesses_made,
    }


@bp.route("/game", methods=("GET", "POST"))
@login_required
def game():
    user_from_db = GameUser.query.filter_by(email=current_user.email).first()

    if request.method == "POST":
        global new_game_obj
        HangmanGame.BAD_GUESSES = 0
        new_game_obj = HangmanGame(user_from_db)
        
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
        guesses_made = HangmanGame.BAD_GUESSES
        if "_" not in selected_word:
            game_status = f"""Congratulations, you won!!!"""
            print(f"You made {HangmanGame.BAD_GUESSES} bad quesses")
            document = get_game_status_data("won", guesses_made)
            result = game_db.collection.insert_one(document)
            print(f"Inserted document with ID: {result.inserted_id}")
            not_used_letters = []
        else:
            game_status = f"""Sorry you lost!
                The word was: '{new_game_obj.game_word}'.
                Do you want to play again?"""
            print(f"You made {HangmanGame.BAD_GUESSES} bad quesses")
            document = get_game_status_data("lost", guesses_made)
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
