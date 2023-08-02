#!/usr/bin/env python3
"""
Basic Flask app with Flask-babel configuration, locale selector, template parametrization,
and user login system
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Union, Dict

app = Flask(__name__)
babel = Babel(app)

# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


# Config class with available language
class Config:
    """
    Represents a Flask Babel configuration.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """
    Determine the best match with the supported languages.
    """
    forced_locale = request.args.get('locale')
    if forced_locale in app.config['LANGUAGES']:
        return forced_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user() -> Union[Dict, None]:
    """
    Get user information from the mock user database.
    """
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id_id))
    return None


@app.before_request
def before_request() -> None:
    """
    Before request hook to find and set the user as a global on flask.g.user.
    """
    user = get_user()
    g.user = user


@app.route('/')
def index():
    """
    Renders the index.html template.
    """
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
