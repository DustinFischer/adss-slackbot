from flask import request

import slack
from api.events import events_api


@events_api.route('/', methods=['POST'])
def events_handler():
    return slack.handler.handle(request)
