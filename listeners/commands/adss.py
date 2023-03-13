from logging import Logger

from slack_bolt import Ack, Respond
from slack_bolt.context.context import BoltContext
from slack_sdk.models.blocks import HeaderBlock, ContextBlock, ImageElement, MarkdownTextObject, SectionBlock, \
    DividerBlock

import adss.models
from adss.service import ADSSService
from utils.static import static
from utils.util import block_id


def adss_slash_command_handler(ack: Ack, context: BoltContext, command, payload, message, respond: Respond,
                               logger: Logger):
    try:
        ack()

        # parse command args
        import re
        options = '|'.join(v.value for v in adss.models.ObjectCategory)
        command_match = re.match(f'({options}) (.*)', command['text'])
        if not command_match:
            raise ValueError()
        obj_cat, name = command_match.groups()
        name = name.strip()
        object_cat = adss.models.ObjectCategory(obj_cat)

        # Fetch for the modelled system... will need some way of figuring how the modelled system is retrieved
        api = ADSSService()
        resp = api.get_object_by_name_preview('Streaming Music', name, object_cat)

        respond(
            blocks=[
                HeaderBlock(
                    block_id=block_id(),
                    text=resp.objectName
                ),
                ContextBlock(
                    block_id=block_id(),
                    elements=[
                        ImageElement(image_url=static.url_for('icons/icon_object_off.png'), alt_text='icon_object'),
                        MarkdownTextObject(text=resp.category.value)
                    ]
                ),
                SectionBlock(
                    block_id=block_id(),
                    text=MarkdownTextObject(text=resp.objectDescription.replace('**', '*'))
                ),
                DividerBlock(),
                ContextBlock(
                    block_id=block_id(),
                    elements=[
                        ImageElement(image_url=static.url_for('icons/icon_people_person.png'), alt_text='icon_people_person'),
                        MarkdownTextObject(text='*Owner*\t'),
                        MarkdownTextObject(text=resp.owner)
                    ]
                ),
                DividerBlock(),
                ContextBlock(
                    block_id=block_id(),
                    elements=[
                        ImageElement(image_url=static.url_for('icons/icon_technologies_off.png'),
                                     alt_text='icon_technologies_off'),
                        MarkdownTextObject(text='*Technologies*\t'),
                        *([ImageElement(image_url=tech.imageLink, alt_text=tech.name) for tech in
                           resp.technologies] or [MarkdownTextObject(text='_no data_')])
                    ]
                ),
                DividerBlock(),
                ContextBlock(
                    block_id=block_id(),
                    elements=[
                        ImageElement(image_url=static.url_for('icons/icon_relationship_hover.png'),
                                     alt_text='icon_relationship_hover'),
                        MarkdownTextObject(text='*Relationships*\t'),
                        MarkdownTextObject(
                            text=f'Calls:{resp.relationships.calls}\nCalled By:{resp.relationships.calledBy}'),
                    ]
                ),
                DividerBlock(),
                ContextBlock(
                    block_id=block_id(),
                    elements=[
                        ImageElement(image_url=static.url_for('icons/icon_data_source.png'), alt_text='icon_data_source'),
                        MarkdownTextObject(text='*Primary Data Sources*\t'),
                        *([MarkdownTextObject(text=(tech.imageKey.value) if tech.imageKey else tech.name) for tech in
                           resp.dataSources] or [MarkdownTextObject(text='_no data_')])

                    ]
                ),
            ]
        )
    except Exception as e:
        logger.error(e)
