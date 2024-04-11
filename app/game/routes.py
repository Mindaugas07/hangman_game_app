from flask import render_template, request, url_for, redirect, Flask
from app.game import bp
from app.extensions import db
from app.models.game.game import HangmanGame
from flask_login import login_required, current_user
import string

app = Flask(__name__)


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

        # print(request.form["letter"])
        player_guess = request.form["letter"]
        new_game_obj.used_letters.add(player_guess)
        guessed_letters = new_game_obj.join_guessed_letters()
        not_used_letters = new_game_obj.not_used_letters(guessed_letters)
        if player_guess not in new_game_obj.game_word:
            HangmanGame.BAD_GUESSES += 1
        print(f" bad guesses {HangmanGame.BAD_GUESSES}")

    selected_word = new_game_obj.guessing_word()

    if new_game_obj.game_over():
        game_status = f"""Sorry you have lost the game!
        The word was: '{new_game_obj.game_word}'.
        Do you want to play again?"""
        not_used_letters = []
        print("Sorry, you lost!")

    return render_template(
        "game/index.html",
        guessed_letters=guessed_letters,
        game_picture="/static/game_images/hangman%d.png" % HangmanGame.BAD_GUESSES,
        selected_word=selected_word,
        not_used_letters=not_used_letters,
        # username=current_user,
        game_status=game_status,
    )
