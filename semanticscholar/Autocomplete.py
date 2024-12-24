from semanticscholar.SemanticScholarObject import SemanticScholarObject


class Autocomplete(SemanticScholarObject):
    '''
    This class abstracts an autocomplete suggestion.
    '''

    def __init__(self, data: dict) -> None:
        super().__init__()
        self._id = None
        self._title = None
        self._authors_year = None
        self._init_attributes(data)

    @property
    def id(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._id

    @property
    def title(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._title

    @property
    def authors_year(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._authors_year

    def _init_attributes(self, data: dict) -> None:
        self._data = data

        if "id" in data:
            self._id = data["id"]

        if "title" in data:
            self._title = data["title"]

        if "authorsYear" in data:
            self._authors_year = data["authorsYear"]
