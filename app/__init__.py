from flask import Flask
from pymongo import MongoClient
from app.models.mongo.mongo import MongoDB

from config import Config
from app.extensions import db
from app.models.user_auth.user_auth import GameUser
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.user_auth import bp as user_bp

    app.register_blueprint(user_bp)

    from app.game import bp as game_bp

    app.register_blueprint(game_bp)

    login_manager = LoginManager(app)
    login_manager.login_view = "user_auth.login"
    login_manager.login_message_category = "info"

    client = MongoClient("mongodb://mongo:27017/")
    db_mongo = client.mydatabase
    collection = db_mongo.mycollection

    try:
        game_db = MongoDB(
            host="localhost",
            port=27017,
            db_name="games_data",
            collection_name="games",
        )
    except:
        print("no db for you")
        # def generate_data_base(1):
        #     for _ in range(1):
        #         self.create_random_person()

    @login_manager.user_loader
    def load_user(user_id):
        db.create_all()
        return GameUser.query.get(int(user_id))

    return app
