import base64
import json
from flask import current_app
from slack_bolt.oauth import OAuthFlow
from slack_bolt.oauth.callback_options import CallbackOptions, SuccessArgs, FailureArgs
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.response.response import BoltResponse

from config import settings
from oauth import log
from oauth.installation_store import get_installation_store


class OauthCallbackOptions(CallbackOptions):

    def __init__(self, *, etc=None):
        self.success = self._handle_success
        self.failure = self._handle_failure

    def _handle_success(self, args: SuccessArgs) -> BoltResponse:
        """
        Define behaviour after slack oauth redirect callback has been successful
        """

        # FIXME: I'm sure there must be a much better way to do this...
        #  This is a quick hack to get the flow working.
        #    How do we reconcile the slack user before and after? Maybe a challenge state param with request to ext auth
        #    that relates to the user (state -> user uuid link?) that created it in the initial redirect after installation?
        install_meta = {
            'enterprise_id': args.installation.enterprise_id,
            'team_id': args.installation.team_id,
            'user_id': args.installation.user_id,
            'is_enterprise_install': args.installation.is_enterprise_install
        }
        install_cookie = base64.b64encode(json.dumps(install_meta).encode('utf-8'))
        url = settings.ADSS_OAUTH_URI
        return BoltResponse(
            status=307,
            body="",
            headers={
                "Content-Type": "text/html; charset=utf-8", "Location": url,
                "Set-Cookie": f"slack-app-install-meta={install_cookie.decode('utf-8')}; " "Secure; " "HttpOnly; " "Path=/; " f"Max-Age={10 * 60 * 60}"
            }
        )

    def _handle_failure(self, args: FailureArgs) -> BoltResponse:
        """
        Define behaviour after slack oauth redirect callback has failed
        """
        # TODO: delete oauth state cookie
        log.debug(f'[OauthCallbackOptions._handle_failure]: request.context {args.request.context.to_copyable()}')
        return BoltResponse(status=args.suggested_status_code, body=f"Installation failed! reason: {args.reason}")


def get_oauth_settings():
    return OAuthSettings(
        client_id=settings.SLACK_CLIENT_ID,
        client_secret=settings.SLACK_CLIENT_SECRET,
        callback_options=OauthCallbackOptions(),
        install_path=settings.SLACK_INSTALL_PATH,
        # url will be used to generate an auth url that redirects to slack oauth
        redirect_uri=settings.SLACK_OAUTH_REDIRECT_URI,
        redirect_uri_path=settings.SLACK_REDIRECT_API_PATH,  # callback path passed to slack oauth on success/failure (would ultimately be called )
        scopes=settings.SLACK_OAUTH_SCOPES,  # minimum required bot user scopes (oauth will request access with scopes)
        user_scopes=settings.SLACK_OAUTH_USER_SCOPES,  # minimum required user scopes (for org installs)
        installation_store=get_installation_store(),
        state_validation_enabled=True,
        state_store=None,  # can customise this, default is to use FileOAuthStateStore
        state_cookie_name=settings.SLACK_OAUTH_STATE_COOKIE_NAME,
        logger=log
    )


def get_oauth_flow():
    return OAuthFlow(
        client=None,  # instance of WebClient to use (one will be created by default)
        settings=get_oauth_settings(),
        logger=log
    )
