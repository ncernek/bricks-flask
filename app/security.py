from flask import abort, Flask, request, current_app
from functools import wraps
from twilio.request_validator import RequestValidator
import os

def validate_twilio_request(func):
    '''
    Validate that incoming requests genuinely originated from Twilio
    source: https://www.twilio.com/docs/usage/tutorials/how-to-secure-your-flask-app-by-validating-incoming-twilio-requests
    '''
    
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # create an instance of the RequestValidator class
        validator = RequestValidator(os.environ.get('TWILIO_AUTH_TOKEN'))

        # validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))
        
        # continue processing the request if it's valid, else 403 error
        if request_valid or current_app.debug:
            return func(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function