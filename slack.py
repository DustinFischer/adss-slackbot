from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler

import listeners
from config import settings

# Slack...
slack = App(
    token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_SIGNING_SECRET
)

handler = SlackRequestHandler(slack)
listeners.register_listeners(slack)
