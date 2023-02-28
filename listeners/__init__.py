from listeners import events

from slack_bolt.app import App


def register_listeners(app: App):
    events.register(app)

