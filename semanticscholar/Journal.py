from typing import Any

from semanticscholar.SemanticScholarObject import SemanticScholarObject


class Journal(SemanticScholarObject):
    '''
    This class represents the Journal where the paper was published.
    '''

    def __init__(self, data) -> None:
        super().__init__()
        self._name = None
        self._pages = None
        self._volume = None
        self._init_attributes(data)

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

    def _init_attributes(self, data):
        self._data = data
        if 'name' in data:
            self._name = data['name']
        if 'pages' in data:
            self._pages = data['pages']
        if 'volume' in data:
            self._volume = data['volume']
