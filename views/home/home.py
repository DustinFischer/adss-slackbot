from slack_sdk.models.blocks import (
    SectionBlock,
    MarkdownTextObject,
    ActionsBlock,
    LinkButtonElement,
    PlainTextObject,
    DividerBlock
)

from . import BaseHomeView


class HomeNoAuthView(BaseHomeView):
    def blocks(self):
        greeting = SectionBlock(
            block_id='sec_home_greeting_upstream_not_connected',
            text=MarkdownTextObject(
                text=f':wave: Hi <@{self.event["user"]}>',
            )
        )

        primer = SectionBlock(
            block_id='sec_home_primer_upstream_not_connected',
            text=MarkdownTextObject(
                text=(
                    'ADSS lets you quickly discover model information.\n'
                    '• Quick access to preview panel level information for any model entity from inside a slack channel.\n'
                    '• Notifications of changes to followed entities'
                )
            )
        )

        connect_button = ActionsBlock(
            elements=[
                LinkButtonElement(
                    text=PlainTextObject(
                        text='Connect ADSS'
                    ),
                    style='primary',
                    url="http://auth.redirect.adss",
                    action_id='connect_upstream_btn'
                )
            ],
            block_id='block_home_upstream_not_connected',
        )

        return [
            greeting,
            primer,
            connect_button,
            DividerBlock()
        ]