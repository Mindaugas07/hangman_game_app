from app.models.user_auth.user_auth import GameUser
from typing import List, Dict
import datetime
from app import game_db


def get_todays_games(user: GameUser) -> List[Dict]:
    todays_games = []
    current_day_of_the_month = datetime.datetime.now().day
    users_played_games = game_db.find_documents(
        {
            "user email": user.email,
        },
        {"_id": 0},
    )
    for game in users_played_games:
        if game["date"].day == current_day_of_the_month:
            todays_games.append(game)
    todays_games_sorted_by_time = sorted(
        todays_games, key=lambda d: d["time"], reverse=True
    )
    return todays_games_sorted_by_time


def todays_games_statistics(user: GameUser) -> Dict:
    game_stats_dict = {}
    games = game_db.query_not_equal("game result", "draw", {"_id": 0})
    wins_by_user = 0
    bad_guesses = 0
    looses_by_user = 0
    for game in games:
        if (
            game["username"] == user.name
            and game["game result"] == "won"
            and game["date"].day == datetime.datetime.now().day
        ):
            wins_by_user += 1
            bad_guesses += game["guesses made"]

        elif (
            game["username"] == user.name
            and game["game result"] == "lost"
            and game["date"].day == datetime.datetime.now().day
        ):
            looses_by_user += 1
            bad_guesses += 6

    game_stats_dict[user.name] = {
        "wins": wins_by_user,
        "losses": looses_by_user,
        "today guesses": bad_guesses,
        "todays games": wins_by_user + looses_by_user,
    }
    return game_stats_dict


def get_user_all_time_statistics(user: GameUser) -> Dict:
    users_all_played_games = game_db.find_documents(
        {"user email": user.email}, {"_id": 0}
    )
    users_all_played_games_sorted_by_time = sorted(
        users_all_played_games, key=lambda d: (d["date"], d["time"]), reverse=True
    )
    return users_all_played_games_sorted_by_time


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
