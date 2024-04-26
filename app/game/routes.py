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
#         new_game_obj = HangmanGame(current_user)
#         print(new_game_obj)
#         print(new_game_obj.obj_to_json())
#         session["new_game_obj"] = new_game_obj.obj_to_json()
#         print(session["new_game_obj"])

#         return redirect("start_game")
#     elif request.method == "GET":
#         return redirect("start_game")


@bp.route("/start_game", methods=("GET", "POST"))
@login_required
def start_game():
    json_dict = session.get("new_game_obj")
    print(json_dict)

    if json_dict is not None:
        print("session yra")
        print(json_dict["game word"])

        new_game_obj = HangmanGame.obj_from_json(json_dict)
        print(new_game_obj)
        guessed_letters = set(json_dict["used letters"])

        print(new_game_obj.used_letters)
        not_used_letters = new_game_obj.not_used_letters(
            guessed_letters=guessed_letters
        )

        if request.method == "POST":
            print("post yra")
            print(new_game_obj.game_status)
            player_guess = request.form["letter"]
            new_game_obj.used_letters.add(player_guess)
            guessed_letters = new_game_obj.join_guessed_letters()
            not_used_letters = new_game_obj.not_used_letters(guessed_letters)
            if player_guess not in new_game_obj.game_word:
                new_game_obj.bad_guesses += 1

        selected_word = new_game_obj.guessing_word()
        print(new_game_obj.user)
        print(new_game_obj.used_letters)
        session["new_game_obj"] = new_game_obj.obj_to_json()

        if new_game_obj.game_over():

            if "_" not in selected_word:
                new_game_obj.insert_game_stats_to_mongo("won")
                not_used_letters = []

            else:
                new_game_obj.insert_game_stats_to_mongo("lost")
                not_used_letters = []
            session.pop("new_game_obj")

            # new_game_obj = HangmanGame(current_user)
            # session["new_game_obj"] = new_game_obj.obj_to_json()
    else:
        print("session nera")
        new_game_obj = HangmanGame(current_user)
        new_game_obj.set_new_game_word()
        guessed_letters = new_game_obj.used_letters
        print(guessed_letters)

        print(new_game_obj.used_letters)
        not_used_letters = new_game_obj.not_used_letters(
            guessed_letters=guessed_letters
        )
        print(not_used_letters)
        selected_word = new_game_obj.guessing_word()
        print(new_game_obj)
        print(new_game_obj.obj_to_json())
        session["new_game_obj"] = new_game_obj.obj_to_json()
        print(session["new_game_obj"])

    return render_template(
        "game/index.html",
        guessed_letters=new_game_obj.used_letters,
        game_picture="/static/game_images/hangman%d.png" % new_game_obj.bad_guesses,
        selected_word=selected_word,
        not_used_letters=not_used_letters,
        game_status=new_game_obj.game_status,
    )
