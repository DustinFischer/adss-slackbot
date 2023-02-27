from os import getenv as env
from dotenv import load_dotenv

load_dotenv()

print('hello i am the config file')

# app configs
HTTP_PORT = int(env('HTTP_PORT', 3000))

# slack configs
SLACK_BOT_TOKEN = env('SLACK_BOT_TOKEN', None)
SLACK_SIGNING_SECRET = env('SLACK_SIGNING_SECRET', None)
SLACK_INSTALL_PATH = env('SLACK_INSTALL_PATH', '/slack/install')
SLACK_REDIRECT_URI_PATH = env('SLACK_REDIRECT_URI_PATH', '/slack/oauth_redirect')

