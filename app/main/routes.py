from flask import render_template
from app.main import bp
from flask_login import LoginManager
from app.models.user_auth.user_auth import GameUser
from app import game_db
from typing import Dict, List
from operator import itemgetter


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

    return all_games_statistics_list(game_stats_dict)
    # return game_stats_dict


def all_games_statistics_list(game_stats_dict: Dict) -> List[List]:
    game_stats_list = []
    game_stats_ordered_list = []
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
        game_stats_list, key=lambda x: (x[1], x[2], -x[3]), reverse=True
    )

    return sorted_game_stats_list


# def ordered_all_games_statistics(
#     user: GameUser,
#     game_stats_dict: Dict,
#     wins_by_user: int,
#     looses_by_user: int,
#     bad_guesses: int,
#     ordered_stats_list: List,
# ):
#     # for user_list in ordered_stats_list:
#     if game_stats_dict[user.name]["wins"] > ordered_stats_list[0][1]:
#         ordered_stats_list.insert(
#             0, [user.name, wins_by_user, looses_by_user, bad_guesses]
#         )
#     elif (
#         game_stats_dict[user.name]["wins"] == ordered_stats_list[0][1]
#         and game_stats_dict[user.name]["losses"] < ordered_stats_list[0][2]
#     ):
#         ordered_stats_list.insert(
#             0, [user.name, wins_by_user, looses_by_user, bad_guesses]
#         )
#     elif (
#         game_stats_dict[user.name]["wins"] == ordered_stats_list[0][1]
#         and game_stats_dict[user.name]["losses"] == ordered_stats_list[0][2]
#         and game_stats_dict[user.name]["total guesses"] < ordered_stats_list[0][3]
#     ):
#         ordered_stats_list.insert(
#             0, [user.name, wins_by_user, looses_by_user, bad_guesses]
#         )

#     else:
#         if game_stats_dict[user.name]["total guesses"] >= ordered_stats_list[0][3]:
#             ordered_stats_list.insert(
#                 0,
#                 [user.name, wins_by_user, looses_by_user, bad_guesses],
#             )

#     return ordered_stats_list


@bp.route("/home")
def home():
    users = GameUser.query.all()
    game_wins = all_games_statistics_dict(users=users)
    try:
        users = GameUser.query.all()
        game_wins = all_games_statistics_dict(users=users)
    except:
        status = "No users detected or no games were played!"
        print(status)
        return render_template("user_auth/index.html", status=status)
    return render_template("user_auth/index.html", users=users, game_wins=game_wins)
