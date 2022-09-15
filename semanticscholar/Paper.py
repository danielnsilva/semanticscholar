from . import Author


class Paper:

    FIELDS = [
        'abstract',
        'authors',
        'citationCount',
        'citations',
        'embedding',
        'externalIds',
        'fieldsOfStudy',
        'influentialCitationCount',
        'isOpenAccess',
        'paperId',
        'referenceCount',
        'references',
        'title',
        'tldr',
        'url',
        'venue',
        'year'
    ]

    SEARCH_FIELDS = [
        'abstract',
        'authors',
        'citationCount',
        'externalIds',
        'fieldsOfStudy',
        'influentialCitationCount',
        'isOpenAccess',
        'paperId',
        'referenceCount',
        'title',
        'url',
        'venue',
        'year'
    ]

    def __init__(self, data) -> None:
        self._abstract = None
        self._authors = None
        self._citationCount = None
        self._citations = None
        self._embedding = None
        self._externalIds = None
        self._fieldsOfStudy = None
        self._influentialCitationCount = None
        self._isOpenAccess = None
        self._paperId = None
        self._referenceCount = None
        self._references = None
        self._title = None
        self._tldr = None
        self._venue = None
        self._year = None
        self._init_attributes(data)

    @property
    def abstract(self) -> str:
        return self._abstract

    @property
    def authors(self) -> list:
        return self._authors

    @property
    def citationCount(self) -> int:
        return self._citationCount

    @property
    def citations(self) -> list:
        return self._citations

    @property
    def embedding(self) -> dict:
        return self._embedding

    @property
    def externalIds(self) -> dict:
        return self._externalIds

    @property
    def fieldsOfStudy(self) -> list:
        return self._fieldsOfStudy

    @property
    def influentialCitationCount(self) -> int:
        return self._influentialCitationCount

    @property
    def isOpenAccess(self) -> bool:
        return self._isOpenAccess

    @property
    def paperId(self) -> str:
        return self._paperId

    @property
    def referenceCount(self) -> int:
        return self._referenceCount

    @property
    def references(self) -> list:
        return self._references

    @property
    def title(self) -> str:
        return self._title

    @property
    def tldr(self) -> dict:
        return self._tldr

    @property
    def url(self) -> str:
        return self._url

    @property
    def venue(self) -> str:
        return self._venue

    @property
    def year(self) -> int:
        return self._year

    def get_raw_data(self) -> dict:
        return self._data

    def _init_attributes(self, data) -> None:
        self._data = data
        if 'abstract' in data:
            self._abstract = data['abstract']
        if 'authors' in data:
            items = []
            for item in data['authors']:
                items.append(Author.Author(item))
            self._authors = items
        if 'citationCount' in data:
            self._citationCount = data['citationCount']
        if 'citations' in data:
            items = []
            for item in data['citations']:
                items.append(Paper(item))
            self._citations = items
        if 'embedding' in data:
            self._embedding = data['embedding']
        if 'externalIds' in data:
            self._externalIds = data['externalIds']
        if 'fieldsOfStudy' in data:
            self._fieldsOfStudy = data['fieldsOfStudy']
        if 'influentialCitationCount' in data:
            self._influentialCitationCount = data['influentialCitationCount']
        if 'isOpenAccess' in data:
            self._isOpenAccess = data['isOpenAccess']
        if 'paperId' in data:
            self._paperId = data['paperId']
        if 'referenceCount' in data:
            self._referenceCount = data['referenceCount']
        if 'references' in data:
            items = []
            for item in data['citations']:
                items.append(Paper(item))
            self._citations = items
        if 'title' in data:
            self._title = data['title']
        if 'tldr' in data:
            self._tldr = data['tldr']
        if 'url' in data:
            self._url = data['url']
        if 'venue' in data:
            self._venue = data['venue']
        if 'year' in data:
            self._year = data['year']
