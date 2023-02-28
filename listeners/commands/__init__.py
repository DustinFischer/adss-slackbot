from .adss import adss_slash_command_handler

from slack_bolt.app import App


def register(app: App):
    app.command('/adss')(adss_slash_command_handler)
