from flask import Flask, request
from flask.logging import default_handler

import slack

from utils.log import get_logger
from config import settings


def create_app():
    # Configure Logger
    default_handler.level = get_logger('slack.adss').level

    # Flask ...
    flask = Flask(__name__)
    flask.config.from_object('config.Config')

    # add CORS?
    # init db

    # register api endpoints...
    from api.events import events_api

    flask.register_blueprint(events_api, url_prefix='/slack/events')

    @flask.route(settings.SLACK_INSTALL_PATH, methods=['GET'])
    def slack_install():
        return slack.handler.handle(request)

    @flask.route(settings.SLACK_OAUTH_REDIRECT_URI_PATH, methods=['GET'])
    def slack_oauth_redirect():
        return slack.handler.handle(request)

    # middlewares...

    flask.logger.debug("App Started with the following endpoints: \n{}".format(
        "\n".join([str(endpoint) + " [" + str(endpoint.methods) + "]" for endpoint in flask.url_map.iter_rules()])
    ))

    return flask


if __name__ == "__main__":
    from config import settings

    create_app().run(port=settings.HTTP_PORT)
