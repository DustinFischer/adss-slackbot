from os import getenv as env
from dotenv import load_dotenv

load_dotenv()

print('hello i am the config file')


SLACK_BOT_TOKEN = env('SLACK_BOT_TOKEN', None)
SLACK_SIGNING_SECRET = env('SLACK_SIGNING_SECRET', None)

HTTP_PORT = int(env('HTTP_PORT', 3000))
