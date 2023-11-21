from typing import Any, Union, List
import asyncio
import nest_asyncio

from semanticscholar.ApiRequester import ApiRequester


class PaginatedResults:
    '''
    Base class that abstracts paginated results from API search.
    You can just iterate over results regardless of the number of pages.
    PaginatedResults and AsyncPaginatedResults inherit from this class, 
    with minor adjustments.
    '''

    def __init__(
                self,
                requester: ApiRequester,
                data_type: Any,
                url: str,
                query: str = None,
                fields: str = None,
                limit: int = None,
                headers: dict = None,
                max_results: int = 10000
            ) -> None:

        self._requester = requester
        self._data_type = data_type
        self._url = url
        self._query = query
        self._fields = fields
        self._limit = limit
        self._headers = headers
        self._max_results = max_results

        self._data = []
        self._total = 0
        self._offset = 0 - self._limit
        self._next = 0
        self._parameters = ''
        self._items = []
        nest_asyncio.apply()
    
    @classmethod
    async def create(
                cls,
                *args, 
                **kwargs
            ):

        obj = cls(
            *args,
            **kwargs
        )
        await obj._async_get_next_page()

        return obj

    @property
    def total(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._total

    @property
    def offset(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._offset

    @property
    def next(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._next

    @property
    def items(self) -> list:
        '''
        :type: :class:`list`
        '''
        return self._items

    @property
    def raw_data(self) -> list:
        '''
        :type: :class:`list`
        '''
        return self._data

    def __iter__(self) -> Any:
        yield from self._items
        while self._has_next_page():
            yield from self._get_next_page()

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, key: int) -> Any:
        return self._items[key]

    def _has_next_page(self) -> bool:
        has_more_results = (self._offset + self._limit) == self._next
        under_limit = (self._offset + self._limit) < (self._max_results - 1)
        return has_more_results and under_limit

    async def _request_data(self) -> Union[dict, List[dict]]:
        return await self._requester.get_data_async(
            self._url,
            self._parameters,
            self._headers
        )

    async def _async_get_next_page(self) -> Union[dict, List[dict]]:
        self._build_params()

        results = await self._request_data()

        return self._update_params(results)

    def _get_next_page(self) -> list:

        self._build_params()

        result_items = []

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(self._request_data())

        return self._update_params(results)

    def _build_params(self) -> None:

        self._parameters = f'query={self._query}' if self._query else ''

        fields = ','.join(self._fields)
        self._parameters += f'&fields={fields}'

        offset = self._offset + self._limit
        self._parameters += f'&offset={offset}'

        total = offset + self._limit
        if total == 10000:
            self._limit -= 1
        self._parameters += f'&limit={self._limit}'

    def _update_params(self, results: Union[dict, List[dict]]) -> list:

        result_items = []

        if 'data' in results:

            self._data = results['data']
            self._total = results['total'] if 'total' in results else 0
            self._offset = results['offset']
            self._next = results['next'] if 'next' in results else 0

            for item in results['data']:
                result_items.append(self._data_type(item))

            self._items += result_items

        return result_items

    def next_page(self) -> None:
        '''
        Get next results
        '''
        self._get_next_page()

    async def async_next_page(self) -> None:
        '''
        Get next results
        '''
        await self._async_get_next_page()
