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

    def keys(self):
        return self._data.keys()

    @property
    def raw_data(self) -> dict:
        '''
        :type: :class:`dict`
        '''
        return self._data
