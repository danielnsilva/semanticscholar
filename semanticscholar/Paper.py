class Paper:

    def __init__(self, data) -> None:
        self._init_attributes(data)

    @property
    def abstract(self) -> str:
        return self._abstract

    @property
    def arxivId(self) -> str:
        return self._arxivId

    @property
    def authors(self) -> list:
        return self._authors

    @property
    def citationVelocity(self) -> int:
        return self._citationVelocity

    @property
    def citations(self) -> int:
        return self._citations

    @property
    def corpusId(self) -> str:
        return self._corpusId

    @property
    def doi(self) -> str:
        return self._doi

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
    def isPublisherLicensed(self) -> bool:
        return self._isPublisherLicensed

    @property
    def is_open_access(self) -> bool:
        return self._isOpenAccess

    @property
    def is_publisher_licensed(self) -> bool:
        return self._isPublisherLicensed

    @property
    def numCitedBy(self) -> int:
        return self._numCitedBy

    @property
    def numCiting(self) -> int:
        return self._numCiting

    @property
    def paperId(self) -> str:
        return self._paperId

    @property
    def references(self) -> list:
        return self._references

    @property
    def title(self) -> str:
        return self._title

    @property
    def topics(self) -> list:
        return self._topics

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
        if 'arxivId' in data:
            self._arxivId = data['arxivId']
        if 'authors' in data:
            self._authors = data['authors']
        if 'citationVelocity' in data:
            self._citationVelocity = data['citationVelocity']
        if 'citations' in data:
            self._citations = data['citations']
        if 'corpusId' in data:
            self._corpusId = data['corpusId']
        if 'doi' in data:
            self._doi = data['doi']
        if 'fieldsOfStudy' in data:
            self._fieldsOfStudy = data['fieldsOfStudy']
        if 'influentialCitationCount' in data:
            self._influentialCitationCount = data['influentialCitationCount']
        if 'isOpenAccess' in data:
            self._isOpenAccess = data['isOpenAccess']
        if 'isPublisherLicensed' in data:
            self._isPublisherLicensed = data['isPublisherLicensed']
        if 'is_open_access' in data:
            self._is_open_access = data['is_open_access']
        if 'is_publisher_licensed' in data:
            self._is_publisher_licensed = data['is_publisher_licensed']
        if 'numCitedBy' in data:
            self._numCitedBy = data['numCitedBy']
        if 'numCiting' in data:
            self._numCiting = data['numCiting']
        if 'paperId' in data:
            self._paperId = data['paperId']
        if 'references' in data:
            self._references = data['references']
        if 'title' in data:
            self._title = data['title']
        if 'topics' in data:
            self._topics = data['topics']
        if 'url' in data:
            self._url = data['url']
        if 'venue' in data:
            self._venue = data['venue']
        if 'year' in data:
            self._year = data['year']
