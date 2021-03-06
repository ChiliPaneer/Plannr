# # Python standard libraries
# import json
# import os
# import sqlite3

# # Third party libraries
# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, url_for, Flask
# )
# from flask_login import (
#     LoginManager,
#     current_user,
#     login_required,
#     login_user,
#     logout_user,
# )
# from oauthlib.oauth2 import WebApplicationClient
# import requests

# # Internal imports
# from db import init_db_command
# from user import User

import os
from flask import Flask
from flask_login import (
    LoginManager,
)
from app.user import User

def create_app(test_config=None):
    """
    The factory function for the whole application which initializes each component
    of the app and connects them to the instantiated Flask app.
    """
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # app.config.from_mapping(
    #     SECRET_KEY=os.environ.get("SECRET_KEY") or os.urandom(24),
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('../app/settings.py', silent=False)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        
    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # @app.route('/')
    # def hello():
    #     return render_template('base.html')

    
    # Flask-Login helper to retrieve a user from our db
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.unauthorized_handler
    def unauthorized():
        return "You must be logged in to access this content.", 403

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    # print(app.config.get("GOOGLE_CLIENT_ID"))
    # print(app.config.get("GOOGLE_CLIENT_SECRET"))
    from . import db
    db.init_app(app)
    with app.app_context():
        from . import auth
        app.register_blueprint(auth.bp)

    from . import calendar
    app.register_blueprint(calendar.bp)
    app.add_url_rule('/', endpoint='index')

    return app