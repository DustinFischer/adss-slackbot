from slack_bolt.oauth import OAuthFlow
from slack_bolt.oauth.callback_options import CallbackOptions, SuccessArgs, FailureArgs
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.response.response import BoltResponse

from config import settings
from oauth.installation_store import get_installation_store

from oauth import log


class OauthCallbackOptions(CallbackOptions):

    def __init__(self, *, etc=None):
        self.success = self._handle_success
        self.failure = self._handle_failure

    def _handle_success(self, args: SuccessArgs) -> BoltResponse:
        """
        Define behaviour after slack oauth redirect callback has been successful
        """
        # TODO: delete oauth state cookie
        # TODO: redirect to third party auth
        log.debug(f'[OauthCallbackOptions._handle_success] installation: {args.installation.to_dict()}')
        return BoltResponse(status=200, body="Installation successful!")

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
        redirect_uri_path=settings.SLACK_OAUTH_REDIRECT_URI_PATH,  # callback path passed to slack oauth on success/failure (would ultimately be called )
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
