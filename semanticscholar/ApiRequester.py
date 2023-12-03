from typing import List, Union

import httpx
import asyncio
import warnings
import inspect
import json
from tenacity import (retry, retry_if_exception_type, stop_after_attempt,
                      wait_fixed)

from semanticscholar.SemanticScholarException import \
    BadQueryParametersException, ObjectNotFoundException


class ApiRequester:

    def __init__(self, timeout, debug) -> None:
        '''
        :param float timeout: an exception is raised \
            if the server has not issued a response for timeout seconds.
        :param bool debug: enable debug mode.
        '''
        self.timeout = timeout
        self.debug = debug

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
    
    @property
    def debug(self) -> bool:
        '''
        :type: :class:`bool`
        '''
        return self._debug
    
    @debug.setter
    def debug(self, debug: bool) -> None:
        '''
        :param bool debug:
        '''
        self._debug = debug
    
    def _curl_cmd(self, url: str, method: str, headers: dict, payload: dict = None) -> str:
        curl_cmd = f'curl -X {method}'
        for key, value in headers.items():
            curl_cmd += f' -H \'{key}: {value}\''
        curl_cmd += f' -d \'{json.dumps(payload)}\'' if payload else ''
        curl_cmd += f' {url}'
        return curl_cmd
    
    def _get_caller_function_name(self) -> str:
        stack = inspect.stack()
        caller = stack[5]
        frame = caller[0]
        info = inspect.getframeinfo(frame)
        return info.function

    def _print_debug(self, url, headers, payload, method) -> None:
        print('-' * 80)
        print(f'Caller function: {self._get_caller_function_name()}')
        print('-' * 80)
        print(f'Method: {method}\n')
        print(f'URL:\n{url}\n')
        print(f'Headers:\n{headers}\n')
        print(f'Payload:\n{payload}\n')
        print(f'cURL command:\n{self._curl_cmd(url, method, headers, payload)}')
        print('-' * 80)

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

        url = f'{url}?{parameters.lstrip("&")}'
        method = 'POST' if payload else 'GET'

        if self.debug:
            self._print_debug(url, headers, payload, method)

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
    