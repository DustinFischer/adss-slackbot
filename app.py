from slack_bolt import App
import config

app = App(
    token=config.SLACK_BOT_TOKEN,
    signing_secret=config.SLACK_SIGNING_SECRET
)

if __name__ == '__main__':
    app.start(port=config.HTTP_PORT)
