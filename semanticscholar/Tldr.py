class Tldr:
    '''
    This class represents auto-generated short summary of the paper from the
    SciTLDR model.
    '''

    def __init__(self, data) -> None:
        self._model = None
        self._text = None
        self._init_attributes(data)

    def __str__(self) -> str:
        return self._text

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def model(self) -> str:
        '''
        :type :class:`str`
        '''
        return self._model

    @property
    def text(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._text

    @property
    def raw_data(self) -> dict:
        '''
        :type: :class:`dict`
        '''
        return self._data

    def _init_attributes(self, data):
        self._data = data
        if 'model' in data:
            self._model = data['model']
        if 'text' in data:
            self._text = data['text']
