from listeners import events

from slack_bolt.app import App


def reigster_listeners(app: App):
    events.register(app)

