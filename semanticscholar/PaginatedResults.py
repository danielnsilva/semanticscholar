from typing import Any

from semanticscholar.ApiRequester import ApiRequester


class PaginatedResults:
    '''
    This class abstracts paginated results from API search.
    You can just iterate over results regardless of the number of pages.
    '''

    def __init__(
                self,
                requester: ApiRequester,
                data_type: Any,
                url: str,
                query: str,
                fields: str,
                limit: int,
                headers: dict = None
            ) -> None:

        self._requester = requester
        self._data_type = data_type
        self._url = url
        self._query = query
        self._fields = fields
        self._limit = limit
        self._headers = headers

        self._data = []
        self._total = 0
        self._offset = 0 - self._limit
        self._next = 0
        self._parameters = ''
        self._items = []

        self.__get_next_page()

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
        while self.__has_next_page():
            yield from self.__get_next_page()

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, key: int) -> Any:
        return self._items[key]

    def __has_next_page(self) -> bool:
        has_any_result = self._total > 0
        has_more_results = (self._offset + self._limit) == self._next
        under_limit = (self._offset + self._limit) < 9999
        return has_any_result and has_more_results and under_limit

    def __get_next_page(self) -> list:

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

        result_items = []
        for item in results['data']:
            result_items.append(self._data_type(item))

        self._items += result_items

        return result_items

    def __build_params(self) -> None:

        self._parameters = f'query={self._query}'

        fields = ','.join(self._fields)
        self._parameters += f'&fields={fields}'

        offset = self._offset + self._limit
        self._parameters += f'&offset={offset}'

        total = offset + self._limit
        if total == 10000:
            self._limit -= 1
        self._parameters += f'&limit={self._limit}'

    def next_page(self) -> None:
        '''
        Get next results
        '''
        self.__get_next_page()
