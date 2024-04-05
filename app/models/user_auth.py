from app.extensions import db

from flask_login import UserMixin
from itsdangerous import SignatureExpired, URLSafeTimedSerializer as Serializer

# from app.user_auth.routes import app


class GameUser(db.Model, UserMixin):
    __tablename__ = "Game user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String(20), unique=True, nullable=False)
    email = db.Column("Email adress", db.String(120), unique=True, nullable=False)
    picture = db.Column("picture", db.String(20), nullable=False, default="default.jpg")
    password = db.Column("Password", db.String(60), unique=True, nullable=False)

    # def get_reset_token(self):
    #     s = Serializer(app.config["SECRET_KEY"])
    #     return s.dumps({"user_id": self.id})

    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(app.config["SECRET_KEY"])
    #     try:
    #         user_id = s.loads(token, max_age=1800)["user_id"]
    #     except:
    #         return None
    #     return GameUser.query.get(user_id)
