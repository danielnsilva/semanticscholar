class Journal:
    '''
    This class represents the Journal where the paper was published.
    '''

    def __init__(self, data) -> None:
        self._name = None
        self._pages = None
        self._volume = None
        self._init_attributes(data)

    @property
    def name(self) -> str:
        '''
        :rtype: :class:`str`
        '''
        return self._name

    @property
    def pages(self) -> str:
        '''
        :rtype: :class:`str`
        '''
        return self._pages

    @property
    def volume(self) -> int:
        '''
        :rtype: :class:`int`
        '''
        return self._volume

    @property
    def raw_data(self) -> dict:
        '''
        :rtype: :class:`dict`
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
