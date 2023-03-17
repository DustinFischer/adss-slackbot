from flask import Flask, request
from flask.logging import default_handler

import slack
from utils.log import get_logger
from config import settings


def create_app():
    # Configure Logger
    default_handler.level = get_logger('slack.adss').level

    # Flask ...
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # add CORS?
    # init db

    with app.app_context():
        # register api endpoints...
        import listeners
        from slack import app as slack_app
        listeners.register_listeners(slack_app)

        from api import slack_api
        app.register_blueprint(slack_api)

        @app.route(settings.SLACK_INSTALL_PATH, methods=['GET'])
        def slack_install():
            return slack.handler.handle(request)

            # middlewares...

        # ...
        app.logger.debug("App Started with the following endpoints: \n{}".format(
            "\n".join([str(endpoint) + " [" + str(endpoint.methods) + "]" for endpoint in app.url_map.iter_rules()])
        ))

        return app


if __name__ == "__main__":
    from config import settings

    create_app().run(port=settings.HTTP_PORT)
