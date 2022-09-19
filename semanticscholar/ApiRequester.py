import requests
from tenacity import (retry,
                      wait_fixed,
                      retry_if_exception_type,
                      stop_after_attempt)

from semanticscholar.SemanticScholarException import BadQueryParametersException


class ApiRequester:
    '''
    This class handles calls to Semantic Scholar API.
    '''

    def __init__(self, timeout) -> None:
        '''
        :param float timeout: an exception is raised
        if the server has not issued a response for timeout seconds.
        '''
        self._timeout = timeout

    def get_timeout(self) -> int:
        '''
        :rtype: :class:`int`
        '''
        return self._timeout

    def set_timeout(self, timeout: int):
        '''
        :param int timeout:
        '''
        self._timeout = timeout

    timeout = property(get_timeout, set_timeout)

    @retry(
        wait=wait_fixed(30),
        retry=retry_if_exception_type(ConnectionRefusedError),
        stop=stop_after_attempt(10)
    )
    def get_data(self, url: str, parameters: str, headers: dict) -> dict:
        '''Get data from Semantic Scholar API

        :param str url: absolute URL to API endpoint.
        :param str parameters: the parameters to add in the URL.
        :param str headers: request headers.
        :returns: data or empty :class:`dict` if not found.
        :rtype: :class:`dict`
        '''

        url = f'{url}?{parameters}'
        r = requests.get(url, timeout=self._timeout, headers=headers)

        data = {}
        if r.status_code == 200:
            data = r.json()
            if len(data) == 1 and 'error' in data:
                data = {}
        elif r.status_code == 400:
            data = r.json()
            raise BadQueryParametersException(data['error'])
        elif r.status_code == 403:
            raise PermissionError('HTTP status 403 Forbidden.')
        elif r.status_code == 429:
            raise ConnectionRefusedError('HTTP status 429 Too Many Requests.')

        return data
