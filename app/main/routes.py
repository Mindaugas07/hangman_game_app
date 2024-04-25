from flask import render_template
from app.main import bp
from app.models.user_auth.user_auth import GameUser
from app import game_db
from typing import Dict, List


def all_games_statistics_dict(users: List[GameUser]) -> Dict:
    game_stats_dict = {}
    games = game_db.query_not_equal("game result", "draw", {"_id": 0})
    for user in users:
        wins_by_user = 0
        bad_guesses = 0
        looses_by_user = 0
        for game in games:
            if game["username"] == user.name and game["game result"] == "won":
                wins_by_user += 1
                bad_guesses += game["guesses made"]

            elif game["username"] == user.name and game["game result"] == "lost":
                looses_by_user += 1
                bad_guesses += 6

        game_stats_dict[user.name] = {
            "wins": wins_by_user,
            "losses": looses_by_user,
            "total guesses": bad_guesses,
        }

    return all_games_statistics_list_sorted(game_stats_dict)


def all_games_statistics_list_sorted(game_stats_dict: Dict[str, Dict]) -> List[List]:
    game_stats_list = []
    for user_dict in game_stats_dict:
        game_stats_list.insert(
            0,
            [
                user_dict,
                game_stats_dict[user_dict]["wins"],
                game_stats_dict[user_dict]["losses"],
                game_stats_dict[user_dict]["total guesses"],
            ],
        )

    sorted_game_stats_list = sorted(
        game_stats_list, key=lambda x: (x[1], -x[2], -x[3]), reverse=True
    )

    return sorted_game_stats_list


@bp.route("/home")
def home():
    try:
        users = GameUser.query.all()
        game_wins = all_games_statistics_dict(users=users)
    except:
        status = "No users detected or no games were played!"
        print(status)
        return render_template("user_auth/index.html", status=status)
    return render_template("user_auth/index.html", users=users, game_wins=game_wins)
