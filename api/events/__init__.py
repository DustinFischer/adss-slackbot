from flask import Blueprint

events_api = Blueprint("events", __name__)

from . import events  # noqa
