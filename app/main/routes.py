from flask import render_template, Flask
from app.main import bp
from app.models.user_auth.user_auth import GameUser
from app.helper_functions.helper_functions import all_games_statistics_dict


app = Flask(__name__)


@bp.route("/home")
def home():

    try:
        users = GameUser.query.all()
        game_wins = all_games_statistics_dict(users=users)[:10]
    except Exception as exception:
        status = "No users detected or no games were played!"
        app.logger.error(
            f" error: {exception} was received while no user or game data could be retrieved 'main.home'! "
        )

        return render_template("user_auth/index.html", status=status)
    return render_template("user_auth/index.html", users=users, game_wins=game_wins)
