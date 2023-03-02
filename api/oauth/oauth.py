import base64
import json

from flask import request, Response
from slack_bolt.adapter.flask.handler import to_flask_response
from slack_bolt.response import BoltResponse

import slack
from api.oauth import oauth_api
from config import settings


@oauth_api.route('/redirect', methods=['GET'])
def slack_oauth_redirect():
    # TODO: fix this. this is a temp workaround to get a valid browser
    # install
    # Redirect to adds login
    # return slack.handler.handle(request)
    if not ('code' in request.args and 'state' in request.args):
        return Response('Missing state / code', status=400)

    try:
        # will return a 307 redirect to ADSS auth
        # sets a 'slack-app-install-meta' cookie with json installation metadata (team, enterprise, user id)
        return slack.handler.handle(request)
    except Exception:
        raise


@oauth_api.route('/redirect/callback', methods=['GET'])
def slack_oauth_redirect_callback():
    # FIXME: is there a better way to do this than this? I'm sure there must be...
    INSTALL_META_COOKIE_NAME = 'slack-app-install-meta'
    install_meta = request.cookies.get(INSTALL_META_COOKIE_NAME, '')
    install_data = base64.b64decode(install_meta).decode('utf-8')
    installation = slack.app.installation_store.find_installation(
        **json.loads(install_data)
    )
    app_id = installation.app_id
    is_enterprise_install = installation.is_enterprise_install
    team_id = installation.team_id
    enterprise_url = installation.enterprise_url

    # Ripped from slack_bolt.oauth.internals.CallbackResponseBuilder
    if is_enterprise_install is True and enterprise_url is not None and app_id is not None:
        url = f"{enterprise_url}manage/organization/apps/profile/{app_id}/workspaces/add"
    elif team_id is None or app_id is None:
        url = "slack://open"
    else:
        url = f"slack://app?team={team_id}&id={app_id}"
    browser_url = f"https://app.slack.com/client/{team_id}"

    html = f"""
        <html>
        <head>
        <meta http-equiv="refresh" content="0; URL={url}">
        <style>
        body {{
          padding: 10px 15px;
          font-family: verdana;
          text-align: center;
        }}
        </style>
        </head>
        <body>
        <h2>Thank you!</h2>
        <p>Redirecting to the Slack App... click <a href="{url}">here</a>. If you use the browser version of Slack, click <a href="{browser_url}" target="_blank">this link</a> instead.</p>
        </body>
        </html>
        """  # noqa: E501

    return to_flask_response(
        BoltResponse(
            status=200,
            headers={
                "Content-Type": "text/html; charset=utf-8",
                "Set-Cookie": f"{settings.SLACK_OAUTH_STATE_COOKIE_NAME}=deleted; " "Secure; " "HttpOnly; " "Path=/; " "Expires=Thu, 01 Jan 1970 00:00:00 GMT",
                "Set-Cookie": f"{INSTALL_META_COOKIE_NAME}=deleted; " "Secure; " "HttpOnly; " "Path=/; " "Expires=Thu, 01 Jan 1970 00:00:00 GMT"
            },
            body=html,
        ))
