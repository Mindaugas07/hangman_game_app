from app.extensions import db

from flask_login import UserMixin


class GameUser(db.Model, UserMixin):
    __tablename__ = "Game user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String(20), unique=True, nullable=False)
    email = db.Column("Email adress", db.String(120), unique=True, nullable=False)
    picture = db.Column("picture", db.String(20), nullable=False, default="default.jpg")
    password = db.Column("Password", db.String(60), unique=True, nullable=False)
