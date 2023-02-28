from logging import Logger

# allowed args: https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
from views.home.home import HomeNoAuthView, UserHomeView


def app_home_opened(client, event, logger: Logger):
    # ignore the app_home_opened event for anything but the Home tab
    if event['tab'] != 'home':
        return

    # handle auth logic
    if True:
        view = HomeNoAuthView(event)

    try:
        client.views_publish(
            user_id=event['user'],
            view=view.view
        )
    except Exception as e:
        logger.error(f'Error publishing home tab: {e}')
