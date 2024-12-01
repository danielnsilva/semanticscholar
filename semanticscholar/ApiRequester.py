import asyncio
import json
import logging
import warnings
from typing import List, Union

import httpx
from tenacity import retry as rerun
from tenacity import retry_if_exception_type, stop_after_attempt, wait_fixed

from semanticscholar.SemanticScholarException import (
    BadQueryParametersException, GatewayTimeoutException,
    InternalServerErrorException, ObjectNotFoundException)

logger = logging.getLogger('semanticscholar')


class ApiRequester:

    def __init__(self, timeout, retry: bool = True) -> None:
        '''
        :param float timeout: an exception is raised 
               if the server has not issued a response for timeout seconds.
        :param bool retry: enable retry mode.
        '''
        self.timeout = timeout
        self.retry = retry

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
    def retry(self) -> bool:
        '''
        :type: :class:`bool`
        '''
        return self._retry
    
    @retry.setter
    def retry(self, retry: bool) -> None:
        '''
        :param bool retry:
        '''
        self._retry = retry

    def _curl_cmd(
                self,
                url: str,
                method: str,
                headers: dict,
                payload: dict = None
            ) -> str:
        curl_cmd = f'curl -X {method}'
        if headers:
            for key, value in headers.items():
                curl_cmd += f' -H \'{key}: {value}\''
        curl_cmd += f' -d \'{json.dumps(payload)}\'' if payload else ''
        curl_cmd += f' {url}'
        return curl_cmd

    async def get_data_async(
        self,
        url: str,
        parameters: str,
        headers: dict,
        payload: dict = None
    ) -> Union[dict, List[dict]]:
        '''
        Get data from Semantic Scholar API

        :param str url: absolute URL to API endpoint.
        :param str parameters: the parameters to add in the URL.
        :param str headers: request headers.
        :param dict payload: data for POST requests.
        :returns: data or empty :class:`dict` if not found.
        :rtype: :class:`dict` or :class:`List` of :class:`dict`
        '''
        if self.retry:
            return await self._get_data_async(
                url, parameters, headers, payload)
        return await self._get_data_async.retry_with(
                stop=stop_after_attempt(1)
            )(self, url, parameters, headers, payload)

    @rerun(
        wait=wait_fixed(30),
        retry=retry_if_exception_type(ConnectionRefusedError),
        stop=stop_after_attempt(10)
    )
    async def _get_data_async(
            self,
            url: str,
            parameters: str,
            headers: dict,
            payload: dict = None
    ) -> Union[dict, List[dict]]:

        parameters=parameters.lstrip("&")
        method = 'POST' if payload else 'GET'

        logger.debug(f'HTTP Request: {method} {url}')
        logger.debug(f'Headers: {headers}')
        logger.debug(f'Payload: {payload}')
        logger.debug(f'cURL command: {self._curl_cmd(url, method, headers, payload)}')

        async with httpx.AsyncClient() as client:
            r = await client.request(
                method, url, params=parameters,timeout=self._timeout, headers=headers,
                json=payload)

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
        elif r.status_code == 500:
            data = r.json()
            raise InternalServerErrorException(data['message'])
        elif r.status_code == 504:
            data = r.json()
            raise GatewayTimeoutException(data['message'])

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
