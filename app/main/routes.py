from flask import render_template
from app.main import bp
from flask_login import LoginManager
from app.models.user_auth.user_auth import GameUser
from app import game_db
from typing import Dict
from datetime import datetime


def game_statistics(users: GameUser) -> Dict:
    game_stats_dict = {}
    game_wins = game_db.query_equal("game result", "won", {"_id": 0})
    game_looses = game_db.query_equal("game result", "lost", {"_id": 0})
    for user in users:
        wins_by_user = 0
        bad_guesses = 0
        looses_by_user = 0
        for game in game_wins:
            if game["username"] == user.name:
                wins_by_user += 1
            try:
                if game["username"] == user.name:
                    bad_guesses += game["guesses made"]
            except:
                bad_guesses = 0

        for game in game_looses:
            if game["username"] == user.name:
                looses_by_user += 1
            try:
                if game["username"] == user.name:
                    bad_guesses += 6
            except:
                bad_guesses = 0

        game_stats_dict[user.name] = {
            "wins": wins_by_user,
            "losses": looses_by_user,
            "total guesses": bad_guesses,
            "today's day": datetime.now().day,
        }
        print(game_stats_dict)
    return game_stats_dict


@bp.route("/home")
def home():
    try:
        users = GameUser.query.all()
        game_wins = game_statistics(users=users)
    except:
        status = "No users detected or no games were played!"
        print(status)
        return render_template("user_auth/index.html", status=status)
    return render_template("user_auth/index.html", users=users, game_wins=game_wins)
