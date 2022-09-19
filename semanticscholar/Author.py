from typing import Any
import semanticscholar.Paper


class Author:
    '''
    This class abstracts an author.
    '''

    FIELDS = [
        'affiliations',
        'aliases',
        'authorId',
        'citationCount',
        'externalIds',
        'hIndex',
        'homepage',
        'name',
        'paperCount',
        'papers',
        'papers.abstract',
        'papers.authors',
        'papers.citationCount',
        'papers.externalIds',
        'papers.fieldsOfStudy',
        'papers.influentialCitationCount',
        'papers.isOpenAccess',
        'papers.journal',
        'papers.paperId',
        'papers.publicationDate',
        'papers.publicationTypes',
        'papers.referenceCount',
        'papers.s2FieldsOfStudy',
        'papers.title',
        'papers.url',
        'papers.venue',
        'papers.year',
        'url'
    ]

    SEARCH_FIELDS = FIELDS

    def __init__(self, data) -> None:
        self._affiliations = None
        self._aliases = None
        self._authorId = None
        self._citationCount = None
        self._externalIds = None
        self._hIndex = None
        self._homepage = None
        self._name = None
        self._paperCount = None
        self._papers = None
        self._url = None
        self._init_attributes(data)

    def __str__(self) -> str:
        return self._data.__str__()

    def __repr__(self) -> Any:
        return self._data.__repr__()

    def __getitem__(self, key) -> Any:
        return self._data.__getitem__(key)

    def keys(self):
        return self._data.keys()

    @property
    def affiliations(self) -> list:
        '''
        :type: :class:`list`
        '''
        return self._affiliations

    @property
    def aliases(self) -> list:
        '''
        :type: :class:`list`
        '''
        return self._aliases

    @property
    def authorId(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._authorId

    @property
    def citationCount(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._citationCount

    @property
    def externalIds(self) -> dict:
        '''
        :type: :class:`dict`
        '''
        return self._externalIds

    @property
    def hIndex(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._hIndex

    @property
    def homepage(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._homepage

    @property
    def name(self) -> str:
        '''
        :type: :class:`int`
        '''
        return self._name

    @property
    def paperCount(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._paperCount

    @property
    def papers(self) -> list:
        '''
        :type: :class:`list`
        '''
        return self._papers

    @property
    def url(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._url

    @property
    def raw_data(self) -> dict:
        '''
        :type: :class:`dict`
        '''
        return self._data

    def _init_attributes(self, data):
        self._data = data
        if 'affiliations' in data:
            self._affiliations = data['affiliations']
        if 'aliases' in data:
            self._aliases = data['aliases']
        if 'authorId' in data:
            self._authorId = data['authorId']
        if 'citationCount' in data:
            self._citationCount = data['citationCount']
        if 'externalIds' in data:
            self._externalIds = data['externalIds']
        if 'hIndex' in data:
            self._hIndex = data['hIndex']
        if 'homepage' in data:
            self._homepage = data['homepage']
        if 'name' in data:
            self._name = data['name']
        if 'paperCount' in data:
            self._paperCount = data['paperCount']
        if 'papers' in data:
            items = []
            for item in data['papers']:
                items.append(semanticscholar.Paper.Paper(item))
            self._papers = items
        if 'url' in data:
            self._url = data['url']
