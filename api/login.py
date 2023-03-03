from flask import Blueprint, request
from slack_bolt.adapter.flask.handler import to_bolt_request, to_flask_response

from slack import app as slack_app

login_api = Blueprint("login", __name__, url_prefix='/login')


@login_api.route('/', methods=['GET'])
def login():
    # TODO: This is the least elegant way I could think to do this.
    #  Just want to reuse what redirects we already have in the oauth api.
    return to_flask_response(
        slack_app.oauth_flow.handle_installation(to_bolt_request(request))
    )
