from os import getenv as env
from dotenv import load_dotenv

from slack_sdk.oauth.state_utils import OAuthStateUtils

load_dotenv()


class Config(object):
    DEBUG = bool(env('DEBUG', True))
    TESTING = False
    CSRF_ENABLED = True
    JSON_SORT_KEYS = False

    # app configs
    HTTP_PORT = int(env('HTTP_PORT', 5000))
    BASE_URL = env('BASE_URL', f'http://localhost:{HTTP_PORT}')

    # slack configs
    # SLACK_BOT_TOKEN = env('SLACK_BOT_TOKEN', None)
    SLACK_CLIENT_ID = env('SLACK_CLIENT_ID', None)
    SLACK_CLIENT_SECRET = env('SLACK_CLIENT_SECRET', None)
    SLACK_SIGNING_SECRET = env('SLACK_SIGNING_SECRET', None)
    SLACK_INSTALL_PATH = env('SLACK_INSTALL_PATH', '/slack/install')

    # oauth ...
    # SLACK_REDIRECT_API_PATH = env('SLACK_OAUTH_REDIRECT_URI_PATH', '/slack/oauth/redirect')
    SLACK_REDIRECT_API_PATH = '/slack/oauth/redirect'
    SLACK_OAUTH_REDIRECT_URI = env('SLACK_OAUTH_REDIRECT_URI', None)
    SLACK_OAUTH_SCOPES = env('SLACK_OAUTH_SCOPES', '').split(',')
    SLACK_OAUTH_USER_SCOPES = env('SLACK_OAUTH_USER_SCOPES', '').split(',')
    SLACK_OAUTH_STATE_COOKIE_NAME = env('SLACK_OAUTH_STATE_COOKIE_NAME', OAuthStateUtils.default_cookie_name)

    # ADSS_OAUTH_URI
    ADSS_OAUTH_URI = env('ADSS_OAUTH_URI', '')
    ADSS_API_BASE_URL = env('ADSS_API_BASE_URL', '')
    ADSS_ACCESS_TOKEN = env('ADSS_API_TOKEN', '')


settings = Config
