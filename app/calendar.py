import json
import os

# Third party libraries
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import requests
from werkzeug.exceptions import abort

from app.user import User

bp = Blueprint('calendar', __name__)

# @bp.route("/")
# def index():
#     """
#     Template index page for the application to display the main page
#     of the web app
#     """
#     db = get_db()
#     posts = db.execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' ORDER BY created DESC'
#     ).fetchall()
#     return render_template('calendar/index.html', posts=posts)

@bp.route("/")
def index():
    """
    Template index page for the application to test whether the
    google login works
    """
    # return render_template('base.html')
    if current_user.is_authenticated:
        g.user = current_user
    return render_template('calendar/index.html')

@bp.route("/group")
def create_group():
    """
    Group view that allows a user to create a group and add users to their group
    based on their email address.
    """

@bp.route("/availability")
def availability():
    """
    Calendar view that generates and depicts the times that the people in the group
    are free.
    """
    