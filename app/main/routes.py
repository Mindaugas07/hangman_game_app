from flask import render_template
from app.main import bp
from app.models.user_auth.user_auth import GameUser
from app import game_db
from typing import Dict, List
from app.helper_functions.helper_functions import all_games_statistics_dict


@bp.route("/home")
def home():
    try:
        users = GameUser.query.all()
        game_wins = all_games_statistics_dict(users=users)[:10]
    except:
        status = "No users detected or no games were played!"
        print(status)
        return render_template("user_auth/index.html", status=status)
    return render_template("user_auth/index.html", users=users, game_wins=game_wins)
