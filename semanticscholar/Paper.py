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

    def __init__(self, data) -> None:
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

    def _init_attributes(self, data) -> None:
        self.data = data
        if 'abstract' in data:
            self._abstract = data['abstract']
        if 'authors' in data:
            self._authors = data['authors']
        if 'citationCount' in data:
            self._citationCount = data['citationCount']
        if 'citations' in data:
            self._citations = data['citations']
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
            self._references = data['references']
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
