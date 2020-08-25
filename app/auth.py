# Python standard libraries
import json
import os

# Third party libraries
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from app.db import init_db_command, get_db
from app.user import User

# import functools
# from werkzeug.security import check_password_hash, generate_password_hash

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Creates the blueprint that will organize the views of the application
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Configuration for the app to be authenticated by Google
# GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
# GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
GOOGLE_CLIENT_ID = current_app.config["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = current_app.config["GOOGLE_CLIENT_SECRET"]
# GOOGLE_DISCOVERY_URL = current_app.config["GOOGLE_DISCOVERY_URL"]
# GOOGLE_CREDENTIALS_JSON = current_app.config["GOOGLE_CREDENTIALS_JSON"]

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

@bp.route("/login")
def login():
    """
    Login view that requests a google login and redirects to google's 
    login page.
    """
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # flow = InstalledAppFlow.from_client_secrets_file(
    #     'credentials.json', SCOPES)
    # creds = flow.run_local_server(port=0)
    # service = build('calendar', 'v3', credentials=creds)

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@bp.route("/login/callback")
def callback():
    """
    The view that google redirects to after you have logged in, which takes the
    response sent by google and tries to create a new User object with the information.
    It handles any errors that may occur and then logs in the user in our app. 
    """
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # Doesn't exist? Add to database
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    # return redirect(url_for("auth.index"))
    return redirect(url_for("index"))


@bp.route("/logout")
@login_required
def logout():
    """
    The logout view which, surprisingly, logs outs the current user 
    and redirects to the index page.
    """
    logout_user()
    return redirect(url_for("index"))


def get_google_provider_cfg():
    """
    Retrieves Google’s provider configuration to help with authentication and
    specifically with OAuth, which google utilizes.
    """
    return requests.get(GOOGLE_DISCOVERY_URL).json()

