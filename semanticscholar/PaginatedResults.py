from typing import Any
from unittest import result
from semanticscholar.ApiRequester import ApiRequester


class PaginatedResults:

    def __init__(
                self,
                requester: ApiRequester,
                data_type: Any,
                url: str,
                query: str,
                fields: str,
                limit: int,
                headers: dict=None
            ) -> None:

        self._requester = requester
        self._data_type = data_type
        self._url = url
        self._query = query
        self._fields = fields
        self._limit = limit
        self._headers = headers

        self._data = list()
        self._total = 0
        self._offset = 0 - self._limit
        self._next = 0      
        self._parameters = ''
        self._items = list()

        self.__get_next_page()

    @property
    def total(self) -> int:
        return self._total

    @property
    def offset(self) -> int:
        return self._offset
    
    @property
    def next(self) -> int:
        return self._next

    @property
    def items(self) -> list:
        return self._items

    @property
    def raw_data(self) -> list:
        return self._data

    def __iter__(self) -> Any:
        yield from self._items
        while self.__has_next_page():
            self.__get_next_page()
            yield from self._items
    
    def __has_next_page(self) -> bool:
        has_any_result = self._total > 0
        reached_limit = (self._offset + self._limit) == self._next
        return has_any_result and reached_limit

    def __get_next_page(self) -> None:

        self.__build_params()

        results = self._requester.get_data(
                self._url,
                self._parameters,
                self._headers
            )

        self._data = results['data']
        self._total = results['total']
        self._offset = results['offset']
        self._next = results['next'] if 'next' in results else 0

        for item in results['data']:
            self._items.append(self._data_type(item))

    def __build_params(self) -> None:
        self._parameters = 'query={}'.format(self._query)
        self._parameters += '&fields={}'.format(','.join(self._fields))
        self._parameters += '&limit={}'.format(self._limit)
        self._parameters += '&offset={}'.format(self._offset + self._limit)

    def next_page(self) -> None:
        self.__get_next_page()
