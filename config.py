from os import getenv as env
from dotenv import load_dotenv

load_dotenv()


class Config(object):
    DEBUG = bool(env('DEBUG', True))
    TESTING = False
    CSRF_ENABLED = True
    JSON_SORT_KEYS = False

    # app configs
    HTTP_PORT = int(env('HTTP_PORT', 5000))

    # slack configs
    SLACK_BOT_TOKEN = env('SLACK_BOT_TOKEN', None)
    SLACK_SIGNING_SECRET = env('SLACK_SIGNING_SECRET', None)
    SLACK_INSTALL_PATH = env('SLACK_INSTALL_PATH', '/slack/install')
    SLACK_REDIRECT_URI_PATH = env('SLACK_REDIRECT_URI_PATH', '/slack/oauth_redirect')


settings = Config
