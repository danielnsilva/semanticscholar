from typing import Any


class SemanticScholarObject:
    '''
    Base class for all API objects.
    '''

    def __init__(self) -> None:
        self._data = None

    def __str__(self) -> str:
        return self._data.__str__()

    def __repr__(self) -> Any:
        return self._data.__repr__()

    def __getitem__(self, key) -> Any:
        return self._data.__getitem__(key)

    def keys(self) -> list:
        '''
        Returns a list of all keys in the API response data.

        :rtype: :class:`list`
        '''
        return self._data.keys()

    @property
    def raw_data(self) -> dict:
        '''
        The API response data in its original JSON structure,
        represented as a `dict`.

        :type: :class:`dict`
        '''
        return self._data
