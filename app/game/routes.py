from flask import render_template, request, url_for, redirect, Flask
from app.game import bp
from app.extensions import db
from app.models.game.game import HangmanGame
from flask_login import login_required
import string

app = Flask(__name__)

new_game = HangmanGame(used_letters=set())


@bp.route("/game", methods=("GET", "POST"))
@login_required
def game():

    bad_guesses = 0
    game_word = new_game.guessing_word()
    guessed_letters = new_game.join_guessed_letters()
    all_letters = string.ascii_lowercase
    if request.method == "POST":
        print(request.form["letter"])
        player_guess = request.form["letter"]
        if player_guess in new_game.game_word:
            new_game.used_letters.add(player_guess)
            print("Great guess!")
        else:
            print("Nope, it's not there.")
            bad_guesses += 1

    selected_word = new_game.guessing_word()

    if bad_guesses == HangmanGame.MAX_GUESSES:
        print("Sorry, you lost!")
    else:
        print("Congratulation! You won the game!")
    # print(f"Your word was: {new_game.game_word}")
    # player_guess = new_game.player_input()
    # if player_guess in new_game.game_word:
    #     print("Great guess!")
    # else:
    #     print("Nope, it's not there.")
    #     bad_guesses += 1

    #     new_game.used_letters.add(player_guess)
    #     selected_word = new_game.guessing_word()

    # draw_hangman(bad_guesses)
    # if bad_guesses == HangmanGame.MAX_GUESSES:
    #     print("Sorry, you lost!")
    # else:
    #     print("Congratulation! You won the game!")
    # print(f"Your word was: {new_game.game_word}")

    return render_template(
        "game/index.html",
        game_word=game_word,
        guessed_letters=guessed_letters,
        game_picture="/static/game_images/kartuves.png",
        all_letters=all_letters,
        selected_word=selected_word,
    )
