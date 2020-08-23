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
from werkzeug.exceptions import abort

from user import User

bp = Blueprint('calendar', __name__)