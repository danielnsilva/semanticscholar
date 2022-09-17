class Tldr:
    '''
    This class represents auto-generated short summary of the paper from the
    SciTLDR model.
    '''

    def __init__(self, data) -> None:
        self._model = None
        self._text = None
        self._init_attributes(data)

    @property
    def model(self) -> str:
        '''
        :rtype: :class:`str`
        '''
        return self._model

    @property
    def text(self) -> str:
        '''
        :rtype: :class:`str`
        '''
        return self._text

    @property
    def raw_data(self) -> dict:
        '''
        :rtype: :class:`dict`
        '''
        return self._data

    def _init_attributes(self, data):
        self._data = data
        if 'model' in data:
            self._model = data['model']
        if 'text' in data:
            self._text = data['text']
