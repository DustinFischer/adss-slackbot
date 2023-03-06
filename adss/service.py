import logging
from urllib import parse

from requests import RequestException
from requests import Response  # noqa
from requests import request
from requests.exceptions import JSONDecodeError

from adss import auth
from config import settings
from models import ObjectPreview

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from models import ObjectCategory


class ADSSRequestError(RequestException):
    pass


class ADSSResponse(object):
    def __init__(self, response):
        # type: (Response) -> None
        self.response = response
        try:
            self.json = response.json()
        except JSONDecodeError:
            self.json = {}

    def __getitem__(self, item):
        return self.json[item]

    @property
    def status_code(self):
        return self.response.status_code

    def raise_on_status(self):
        if self.status_code >= 400:
            logger.debug(f"error json: {self.json} ")
            raise ADSSRequestError(f"Error {self.status_code}: {self.json}", response=self.response)


class ADSSService(object):
    """
    HTTP client service facade for interacting with ADSS Api
    """

    def __init__(self, override_base_url=None, cookies=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.override_base_url = override_base_url
        self.cookies = cookies

    @staticmethod
    def get_url(url_key, default_url_key=None):
        """get keyed relpath from stored"""
        raise NotImplementedError()

    def get_base_url(self):
        return settings.ADSS_API_BASE_URL

    def url(self, relpath):
        base_url = self.get_base_url()
        return '{}/{}'.format(base_url, parse.quote(relpath, safe='/'))

    def _request(self, method, path, data=None, params=None) -> ADSSResponse:
        auth_header = dict(
            access_token=auth.get_access_token(user='TEST')  # FIXME: this is very quick and blunt
        )

        res = request(
            method=method.upper(),
            url=self.url(path),
            data=data,
            params=params,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                **auth_header
            },
            cookies=self.cookies
        )
        return ADSSResponse(res)

    def get(self, path, params=None):
        return self._request('get', path, params=params)

    def post(self, path, data=None):
        return self._request('post', path, data=data)

    def patch(self, path, data=None):
        return self._request('patch', path, data=data)

    def get_object_by_name_preview(self, modelled_system: str, object_name, category: ObjectCategory):
        res = self.get(f'models/{modelled_system}/objects/{object_name}:{category.value}/preview')
        res.raise_on_status()
        return ObjectPreview(**res.json)


API = ADSSService()

if __name__ == '__main__':
    API.get_object_by_name_preview('Streaming Music', 'CDN', ObjectCategory.SERVICE)
