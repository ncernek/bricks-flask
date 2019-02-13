'''this blueprint gets added as an extension to the main Flask app in __init__'''
import os
from datetime import timedelta
from flask import Blueprint, current_app, session
from app import chat 
from app import notify
from app import authenticate
from app.security import validate_twilio_request, validate_google_cron_request

main = Blueprint('main', __name__)


@main.route( "/chat", methods=['GET', 'POST'])
@validate_twilio_request
def conduct_conversations_wrapper():
    return chat.main()

@main.route("/")
def landing_page():
    return f"""
<plaintext>

   welcome to Bricks.

         _______
      __/______/|___  
    /___|__ ___|/__/|
    |______|_______|/


Please text {os.environ.get('TWILIO_PHONE_NUMBER')} to get started.
"""

@main.route("/notify", methods=['GET'])
@validate_google_cron_request
def send_notifications_wrapper():
    return notify.main()


@main.route("/authenticate", methods=['POST'])
def authenticate_user_wrapper():
    return authenticate.main()


# TODO(Nico) is this the right place to put this?
@current_app.before_request
def session_timeout():
    session.permanent = True
    current_app.permanent_session_lifetime = timedelta(seconds=10)