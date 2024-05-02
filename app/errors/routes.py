from app.main import bp
from flask import render_template


@bp.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404
