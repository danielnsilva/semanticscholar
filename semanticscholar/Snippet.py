from semanticscholar.SemanticScholarObject import SemanticScholarObject


class SnippetPaper(SemanticScholarObject):
    '''
    Basic paper data returned by the snippet search endpoint.
    '''

    def __init__(self, data: dict) -> None:
        super().__init__()
        self._corpus_id = None
        self._title = None
        self._authors = None
        self._open_access_info = None
        self._init_attributes(data)

    @property
    def corpus_id(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._corpus_id

    @property
    def title(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._title

    @property
    def authors(self) -> list:
        '''
        :type: :class:`list` of :class:`str`
        '''
        return self._authors

    @property
    def open_access_info(self) -> dict:
        '''
        Open access info (license, status, disclaimer).

        :type: :class:`dict`
        '''
        return self._open_access_info

    def _init_attributes(self, data: dict) -> None:
        self._data = data

        if 'corpusId' in data:
            self._corpus_id = data['corpusId']

        if 'title' in data:
            self._title = data['title']

        if 'authors' in data:
            self._authors = data['authors']

        if 'openAccessInfo' in data:
            self._open_access_info = data['openAccessInfo']


class SnippetText(SemanticScholarObject):
    '''
    Text snippet data returned by the snippet search endpoint.
    '''

    def __init__(self, data: dict) -> None:
        super().__init__()
        self._text = None
        self._snippet_kind = None
        self._section = None
        self._snippet_offset = None
        self._annotations = None
        self._init_attributes(data)

    @property
    def text(self) -> str:
        '''
        The direct quote or snippet text from the paper.

        :type: :class:`str`
        '''
        return self._text

    @property
    def snippet_kind(self) -> str:
        '''
        Where the snippet is located: title, abstract, or body.

        :type: :class:`str`
        '''
        return self._snippet_kind

    @property
    def section(self) -> str:
        '''
        Section of the paper where the snippet is located
        (only for body snippets).

        :type: :class:`str`
        '''
        return self._section

    @property
    def snippet_offset(self) -> dict:
        '''
        Location of the snippet within the paper (start, end).

        :type: :class:`dict`
        '''
        return self._snippet_offset

    @property
    def annotations(self) -> dict:
        '''
        Annotations (sentences, refMentions).

        :type: :class:`dict`
        '''
        return self._annotations

    def _init_attributes(self, data: dict) -> None:
        self._data = data

        if 'text' in data:
            self._text = data['text']

        if 'snippetKind' in data:
            self._snippet_kind = data['snippetKind']

        if 'section' in data:
            self._section = data['section']

        if 'snippetOffset' in data:
            self._snippet_offset = data['snippetOffset']

        if 'annotations' in data:
            self._annotations = data['annotations']


class Snippet(SemanticScholarObject):
    '''
    This class abstracts a snippet search result.
    '''

    def __init__(self, data: dict) -> None:
        super().__init__()
        self._score = None
        self._paper = None
        self._snippet = None
        self._init_attributes(data)

    @property
    def score(self) -> float:
        '''
        Relevance score of the snippet match.

        :type: :class:`float`
        '''
        return self._score

    @property
    def paper(self) -> SnippetPaper:
        '''
        Basic paper data.

        :type: :class:`semanticscholar.Snippet.SnippetPaper`
        '''
        return self._paper

    @property
    def snippet(self) -> SnippetText:
        '''
        Snippet data.

        :type: :class:`semanticscholar.Snippet.SnippetText`
        '''
        return self._snippet

    @property
    def text(self) -> str:
        '''
        Shortcut for snippet.text.

        :type: :class:`str`
        '''
        if self._snippet:
            return self._snippet.text
        return None

    def _init_attributes(self, data: dict) -> None:
        self._data = data

        if 'score' in data:
            self._score = data['score']

        if 'paper' in data:
            self._paper = SnippetPaper(data['paper'])

        if 'snippet' in data:
            self._snippet = SnippetText(data['snippet'])
