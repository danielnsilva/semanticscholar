from typing import List, Union

import httpx
import asyncio
import warnings
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_fixed)

from semanticscholar.SemanticScholarException import \
    BadQueryParametersException, ObjectNotFoundException


class ApiRequester:

    def __init__(self, timeout) -> None:
        '''
        :param float timeout: an exception is raised \
            if the server has not issued a response for timeout seconds.
        '''
        self.timeout = timeout

    @property
    def timeout(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: int) -> None:
        '''
        :param int timeout:
        '''
        self._timeout = timeout

    @retry(
        wait=wait_fixed(30),
        retry=retry_if_exception_type(ConnectionRefusedError),
        stop=stop_after_attempt(10)
    )
    async def get_data_async(
                self,
                url: str,
                parameters: str,
                headers: dict,
                payload: dict = None
            ) -> Union[dict, List[dict]]:
        '''Get data from Semantic Scholar API

        :param str url: absolute URL to API endpoint.
        :param str parameters: the parameters to add in the URL.
        :param str headers: request headers.
        :param dict payload: data for POST requests.
        :returns: data or empty :class:`dict` if not found.
        :rtype: :class:`dict` or :class:`List` of :class:`dict`
        '''

        url = f'{url}?{parameters}'
        method = 'POST' if payload else 'GET'

        async with httpx.AsyncClient() as client:
            r = await client.request(
                method, url, timeout=self._timeout, headers=headers, json=payload)

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
        elif r.status_code == 404:
            data = r.json()
            raise ObjectNotFoundException(data['error'])
        elif r.status_code == 429:
            raise ConnectionRefusedError('HTTP status 429 Too Many Requests.')
        elif r.status_code in [500, 504]:
            data = r.json()
            raise Exception(data['message'])

        return data
    
    def get_data(
                self,
                url: str,
                parameters: str,
                headers: dict,
                payload: dict = None
            ) -> Union[dict, List[dict]]:
        warnings.warn(
            "get_data() is deprecated and will be disabled in the future," +
            " use the async version instead.",
            DeprecationWarning
            )

        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            self.get_data_async(
                url=url,
                parameters=parameters,
                headers=headers,
                payload=payload
            )
        )
    