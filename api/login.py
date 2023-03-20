from flask import Blueprint, request
from slack_bolt.adapter.flask.handler import to_bolt_request, to_flask_response

from oauth.oauth import get_oauth_settings, get_oauth_flow

login_api = Blueprint("login", __name__, url_prefix='/login')


def get_login_oauth_flow():
    settings = get_oauth_settings(install_render=False)
    return get_oauth_flow(oauth_settings=settings)


@login_api.route('/', methods=['GET'])
def login():
    login_oauth_flow = get_login_oauth_flow()
    return to_flask_response(
        login_oauth_flow.handle_installation(to_bolt_request(request))
    )
