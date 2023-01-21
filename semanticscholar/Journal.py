from typing import Any


class Journal:
    '''
    This class represents the Journal where the paper was published.
    '''

    def __init__(self, data) -> None:
        self._name = None
        self._pages = None
        self._volume = None
        self._init_attributes(data)

    def __str__(self) -> str:
        return f'{self._name}'

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, key) -> Any:
        return self._data.__getitem__(key)

    def keys(self):
        return self._data.keys()

    @property
    def name(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._name

    @property
    def pages(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._pages

    @property
    def volume(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._volume

    @property
    def raw_data(self) -> dict:
        '''
        :type: :class:`dict`
        '''
        return self._data

    def _init_attributes(self, data):
        self._data = data
        if 'name' in data:
            self._name = data['name']
        if 'pages' in data:
            self._pages = data['pages']
        if 'volume' in data:
            self._volume = data['volume']
