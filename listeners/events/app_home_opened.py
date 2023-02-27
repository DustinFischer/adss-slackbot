from logging import Logger

from slack_sdk.models import blocks
from slack_sdk.models import views


# allowed args: https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
def app_home_opened(client, event, logger: Logger):
    # ignore the app_home_opened event for anything but the Home tab
    if event['tab'] != 'home':
        return
    greeting = blocks.SectionBlock(
        block_id='home_greeting_not_connected',
        text=blocks.MarkdownTextObject(
            text=f':wave: Hi <@{event["user"]}>',
        )
    )
    primer = blocks.SectionBlock(
        block_id='home_primer_not_connected',
        text=blocks.MarkdownTextObject(
            text='ADSS lets you see stuff about your organization.',
        )

    )
    connect_button = blocks.ActionsBlock(
        elements=[
            blocks.LinkButtonElement(
                text=blocks.PlainTextObject(
                    text='Connect ADSS'
                ),
                style='primary',
                url="http://auth.redirect.adss",
                action_id='connect_adss_btn'
            )
        ],
        block_id='block_home_not_connected',
    )

    view = views.View(
        type='home',
        # id='home_not_connected',
        blocks=[
            greeting,
            primer,
            connect_button
        ],
        # TODO: home view state??
    )

    try:
        client.views_publish(
            user_id=event['user'],
            view=view
        )
    except Exception as e:
        logger.error(f'Error publishing home tab: {e}')
