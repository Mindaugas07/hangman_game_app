from flask import render_template, request, redirect, Flask, session
from app.game import bp
from app.models.game.game import HangmanGame
from app.models.user_auth.user_auth import GameUser
from flask_login import login_required, current_user
import string
from app import game_db
import json


app = Flask(__name__)


# @bp.route("/game", methods=("GET", "POST"))
# @login_required
# def game():

#     if request.method == "POST":
#         # global new_game_obj
#         HangmanGame.BAD_GUESSES = 0
#         new_game_obj = HangmanGame(current_user)
#         print(new_game_obj)
#         session["new_game_obj"] = new_game_obj.obj_to_json()
#         # session["new_game_obj"] = new_game_obj

#         return redirect("start_game")
#     else:
#         return render_template("game/new_game.html")


@bp.route("/start_game", methods=("GET", "POST"))
@login_required
def start_game():
    # HangmanGame.BAD_GUESSES = 0
    # new_game_obj = HangmanGame(current_user)
    json_dict = session.get("new_game_obj")
    # print(session.get("new_game_obj"))

    # print(used_letters)
    if json_dict is None:
        print("session nera")
        HangmanGame.BAD_GUESSES = 0
        new_game_obj = HangmanGame(current_user)
        used_letters = string.ascii_lowercase

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
                new_game_obj.insert_game_stats_to_mongo("won")

            else:
                new_game_obj.insert_game_stats_to_mongo("lost")
        else:
            HangmanGame.BAD_GUESSES = 0
            new_game_obj = HangmanGame(current_user)

    else:
        print("session yra")
        used_letters = set(json_dict["used letters"])
        new_game_obj = HangmanGame(
            user=json_dict["username"],
            game_status=None,
            used_letters=set(json_dict["used letters"]),
            game_word=json_dict["game word"],
        )

        print(new_game_obj)
        not_used_letters = new_game_obj.not_used_letters(used_letters)

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
                new_game_obj.insert_game_stats_to_mongo("won")

            else:
                new_game_obj.insert_game_stats_to_mongo("lost")
        else:
            HangmanGame.BAD_GUESSES = 0
            new_game_obj = HangmanGame(current_user)

    return render_template(
        "game/index.html",
        guessed_letters=new_game_obj.used_letters,
        game_picture="/static/game_images/hangman%d.png" % HangmanGame.BAD_GUESSES,
        selected_word=selected_word,
        not_used_letters=not_used_letters,
        game_status=new_game_obj.game_status,
    )
