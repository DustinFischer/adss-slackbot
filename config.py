import base64
from os import getenv as env

from dotenv import load_dotenv
from slack_sdk.oauth.state_utils import OAuthStateUtils

load_dotenv()


class Config(object):
    DEBUG = bool(env('DEBUG', True))
    TESTING = False
    CSRF_ENABLED = True
    JSON_SORT_KEYS = False


class Settings:
    # app configs
    HTTP_PORT = int(env('HTTP_PORT', 5000))
    BASE_URL = env('BASE_URL', f'http://localhost:{HTTP_PORT}')

    # slack configs
    SLACK_CLIENT_ID = env('SLACK_CLIENT_ID', None)
    SLACK_CLIENT_SECRET = env('SLACK_CLIENT_SECRET', None)
    SLACK_SIGNING_SECRET = env('SLACK_SIGNING_SECRET', None)
    SLACK_INSTALL_PATH = env('SLACK_INSTALL_PATH', '/slack/install')

    # oauth ...
    SLACK_REDIRECT_PATH = env('SLACK_REDIRECT_PATH', '/slack/oauth/redirect')
    SLACK_OAUTH_REDIRECT_URI = env('SLACK_OAUTH_REDIRECT_URI', f'{BASE_URL}{SLACK_REDIRECT_PATH}')
    SLACK_OAUTH_SCOPES = env('SLACK_OAUTH_SCOPES', 'channels:history,chat:write,commands,incoming-webhook').split(',')
    SLACK_OAUTH_USER_SCOPES = env('SLACK_OAUTH_USER_SCOPES', '').split(',')
    SLACK_OAUTH_STATE_COOKIE_NAME = env('SLACK_OAUTH_STATE_COOKIE_NAME', OAuthStateUtils.default_cookie_name)
    SLACK_REDIRECT_CALLBACK_PATH = env('SLACK_REDIRECT_CALLBACK_PATH', '/slack/oauth/redirect/callback')
    SLACK_REDIRECT_CALLBACK_URI = env('SLACK_REDIRECT_CALLBACK_URI', f'{BASE_URL}{SLACK_REDIRECT_CALLBACK_PATH}')

    # ADSS Settings...
    ADSS_OAUTH_URI = env('ADSS_OAUTH_URI', f'https://signin.adss-eng-develop.spandigital.net/login/spandigital?redir={base64.b64encode(SLACK_REDIRECT_CALLBACK_URI.encode()).decode()}')
    ADSS_API_BASE_URL = env('ADSS_API_BASE_URL', 'https://spandigital.adss-eng-develop.spandigital.net/api/v2')
    ADSS_API_TOKEN = env('ADSS_API_TOKEN', '')  # ADSS oauth_token jwt, get this from browser cookie (workaround)
    ADSS_MODEL = env('ADSS_MODEL', 'Streaming Music')


settings = Settings
