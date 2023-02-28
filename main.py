from flask import Flask
from flask.logging import default_handler

from utils.log import get_logger


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

    # middlewares...

    flask.logger.debug("App Started with the following endpoints: \n{}".format(
        "\n".join([str(endpoint) + " [" + str(endpoint.methods) + "]" for endpoint in flask.url_map.iter_rules()])
    ))

    return flask


if __name__ == "__main__":
    from config import settings

    create_app().run(port=settings.HTTP_PORT)
