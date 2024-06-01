from semanticscholar.SemanticScholarObject import SemanticScholarObject


class Tldr(SemanticScholarObject):
    '''
    This class represents auto-generated short summary of the paper from the
    SciTLDR model.
    '''

    def __init__(self, data) -> None:
        super().__init__()
        self._model = None
        self._text = None
        self._init_attributes(data)

    @property
    def model(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._model

    @property
    def text(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._text

    def _init_attributes(self, data):
        self._data = data
        if 'model' in data:
            self._model = data['model']
        if 'text' in data:
            self._text = data['text']
