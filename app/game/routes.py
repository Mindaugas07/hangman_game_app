from flask import render_template, request, url_for, redirect, Flask
from app.game import bp
from app.extensions import db
from app.models.game.game import HangmanGame
from flask_login import login_required, current_user
import string

app = Flask(__name__)

new_game = HangmanGame(used_letters=set())


@bp.route("/game", methods=("GET", "POST"))
@login_required
def game():
    game_status = None

    guessed_letters = new_game.join_guessed_letters()
    not_used_letters = list(string.ascii_lowercase)

    if request.method == "POST":
        print(request.form["letter"])
        player_guess = request.form["letter"]
        new_game.used_letters.add(player_guess)
        guessed_letters = new_game.join_guessed_letters()
        # print(f"player guess is {player_guess}")
        # print(f"not guessed letters is {not_used_letters}")
        # print(f"used letters is {guessed_letters}")
        not_used_letters = new_game.not_used_letters(guessed_letters)
        # print(not_used_letters)
        if player_guess in new_game.game_word:
            print("Great guess!")
        else:
            print("Nope, it's not there.")
            HangmanGame.BAD_GUESSES += 1
        print(f" bad guesses {HangmanGame.BAD_GUESSES}")

    selected_word = new_game.guessing_word()

    if new_game.game_over():
        game_status = """Sorry you have lost the game!
        Do you wat to play again?"""
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
