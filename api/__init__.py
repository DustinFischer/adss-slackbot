from flask import Blueprint

slack_api = Blueprint("slack", __name__, url_prefix='/slack')

from api.events import events_api  # noqa
from api.oauth import oauth_api  # noqa

slack_api.register_blueprint(events_api)
slack_api.register_blueprint(oauth_api)
