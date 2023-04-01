from semanticscholar.Paper import Paper
from semanticscholar.SemanticScholarObject import SemanticScholarObject


class BaseReference(SemanticScholarObject):
    '''
    Base class for both Citation and Reference classes.
    '''

    FIELDS = [
        'contexts',
        'intents',
        'isInfluential'
    ]

    def __init__(self, data: dict) -> None:
        super().__init__()
        self._contexts = None
        self._intents = None
        self._isInfluential = None
        self._paper = None
        self._init_attributes(data)

    @property
    def contexts(self) -> list:
        '''
        :type: :class:`list`
        '''
        return self._contexts

    @property
    def intents(self) -> list:
        '''
        :type: :class:`list`
        '''
        return self._intents

    @property
    def isInfluential(self) -> bool:
        '''
        :type: :class:`bool`
        '''
        return self._isInfluential

    @property
    def paper(self) -> Paper:
        '''
        :type: :class:`semanticscholar.Paper.Paper`
        '''
        return self._paper

    def _init_attributes(self, data: dict) -> None:
        self._data = data
        if 'contexts' in data:
            self._contexts = data['contexts']
        if 'intents' in data:
            self._intents = data['intents']
        if 'isInfluential' in data:
            self._isInfluential = data['isInfluential']
