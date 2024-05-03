from flask import render_template, request, redirect, Flask, session, url_for, abort
from app.game import bp
from playsound import playsound

from app.game.game import HangmanGame
from app.models.user_auth.user_auth import GameUser
from flask_login import login_required, current_user


app = Flask(__name__)


@bp.route("/game")
@login_required
def game():
    if session.get("new_game_obj") == None:

        new_game_obj = HangmanGame(current_user)
        new_game_obj.set_new_game_word()
        session["new_game_obj"] = new_game_obj.obj_to_json()

    return redirect(url_for("game.start_game"))


@bp.route("/start_game", methods=("GET", "POST"))
@login_required
def start_game():

    json_dict = session.get("new_game_obj")

    if json_dict is not None:
        print(json_dict["game word"])

        new_game_obj = HangmanGame.obj_from_json(json_dict)
        guessed_letters = set(json_dict["used letters"])
        not_used_letters = new_game_obj.not_used_letters(
            guessed_letters=guessed_letters
        )

        if request.method == "POST":
            player_guess = request.form["letter"]
            new_game_obj.used_letters.add(player_guess)
            guessed_letters = new_game_obj.join_guessed_letters()
            not_used_letters = new_game_obj.not_used_letters(guessed_letters)
            if player_guess not in new_game_obj.game_word:
                playsound("app/static/sounds/wrong.mp3")
                new_game_obj.bad_guesses += 1
            else:
                playsound("app/static/sounds/correct.mp3")

        selected_word = new_game_obj.guessing_word()
        session["new_game_obj"] = new_game_obj.obj_to_json()

        if new_game_obj.game_over():
            if "_" not in selected_word:
                new_game_obj.insert_game_stats_to_mongo("won")
                not_used_letters = []

            else:
                new_game_obj.insert_game_stats_to_mongo("lost")
                not_used_letters = []
            session.pop("new_game_obj")

    try:
        return render_template(
            "game/index.html",
            guessed_letters=new_game_obj.used_letters,
            game_picture="/static/game_images/hangman%d.png" % new_game_obj.bad_guesses,
            selected_word=selected_word,
            not_used_letters=not_used_letters,
            game_status=new_game_obj.game_status,
        )
    except Exception as exception:
        app.logger.fatal(
            f" error: {exception} was received while game data did not load in route game.start_game! "
        )

        return render_template("errors/404.html")
