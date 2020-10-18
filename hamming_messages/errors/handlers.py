"""Import flask."""
from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def page_not_found(error):
    """Page not found page."""
    print(error)
    return render_template("errors/404.pug"), 404


@errors.app_errorhandler(500)
def internal_error(error):
    """Internal error page."""
    print(error)
    return render_template("errors/500.pug"), 500
