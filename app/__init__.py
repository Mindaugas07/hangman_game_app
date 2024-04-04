from flask import Flask

from config import Config
from app.extensions import db
from flask import render_template, redirect, url_for, flash, request


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from flask_bcrypt import Bcrypt
    from flask_mail import Mail
    from flask_login import LoginManager, current_user
    from app.models.user_login import GameUser

    bcrypt = Bcrypt(app)
    mail = Mail(app)
    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        db.create_all()
        return GameUser.query.get(int(user_id))

    from app.forms import forms

    @app.route("/register", methods=["GET", "POST"])
    def register():
        db.create_all()
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = forms.RegistrationForm()
        if form.validate_on_submit():
            encrypted_password = bcrypt.generate_password_hash(
                form.password.data
            ).decode("utf-8")
            user = GameUser(
                name=form.name.data,
                email=form.email.data,
                password=encrypted_password,
            )
            db.session.add(user)
            db.session.commit()
            flash("You succusesfuly registered! You may login.", "success")
            return redirect(url_for("index"))
        return render_template("register.html", title="Register", form=form)

    return app
