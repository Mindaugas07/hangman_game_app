from flask import render_template
from app.main import bp
from flask_login import (
    LoginManager,
    current_user,
    logout_user,
    login_user,
    login_required,
)
from app.models.user_auth.user_auth import GameUser
from app import game_db
from typing import Dict


def number_of_wins_by_player(users: GameUser) -> int:
    game_win_list = []

    game_wins = game_db.query_equal("game result", "won", {"_id": 0})
    for user in users:
        wins_by_user = 0
        for game in game_wins:
            if game["userame"] == user.name:
                wins_by_user += 1
        game_win_list.append(f"user {user.name} has won {wins_by_user}")
    return game_win_list


@bp.route("/home")
def home():
    users = GameUser.query.all()
    game_wins = number_of_wins_by_player(users=users)

    return render_template("user_auth/index.html", users=users, game_wins=game_wins)
