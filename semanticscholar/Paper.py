from datetime import datetime
from typing import Any
import semanticscholar.Author
import semanticscholar.Journal
import semanticscholar.Tldr


class Paper:
    '''
    This class abstracts a paper.
    '''

    FIELDS = [
        'abstract',
        'authors',
        'authors.affiliations',
        'authors.aliases',
        'authors.authorId',
        'authors.citationCount',
        'authors.externalIds',
        'authors.hIndex',
        'authors.homepage',
        'authors.name',
        'authors.paperCount',
        'authors.url',
        'citationCount',
        'citations',
        'citations.abstract',
        'citations.authors',
        'citations.citationCount',
        'citations.externalIds',
        'citations.fieldsOfStudy',
        'citations.influentialCitationCount',
        'citations.isOpenAccess',
        'citations.journal',
        'citations.paperId',
        'citations.publicationDate',
        'citations.publicationTypes',
        'citations.referenceCount',
        'citations.s2FieldsOfStudy',
        'citations.title',
        'citations.url',
        'citations.venue',
        'citations.year',
        'embedding',
        'externalIds',
        'fieldsOfStudy',
        'influentialCitationCount',
        'isOpenAccess',
        'journal',
        'paperId',
        'publicationDate',
        'publicationTypes',
        'referenceCount',
        'references',
        'references.abstract',
        'references.authors',
        'references.citationCount',
        'references.externalIds',
        'references.fieldsOfStudy',
        'references.influentialCitationCount',
        'references.isOpenAccess',
        'references.journal',
        'references.paperId',
        'references.publicationDate',
        'references.publicationTypes',
        'references.referenceCount',
        'references.s2FieldsOfStudy',
        'references.title',
        'references.url',
        'references.venue',
        'references.year',
        's2FieldsOfStudy',
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
        'journal',
        'paperId',
        'publicationDate',
        'publicationTypes',
        'referenceCount',
        's2FieldsOfStudy',
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
        self._journal = None
        self._paperId = None
        self._publicationDate = None
        self._publicationTypes = None
        self._referenceCount = None
        self._references = None
        self._s2FieldsOfStudy = None
        self._title = None
        self._tldr = None
        self._venue = None
        self._year = None
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
    def abstract(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._abstract

    @property
    def authors(self) -> list:
        '''
        :type: :class:`list`
        '''
        return self._authors

    @property
    def citationCount(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._citationCount

    @property
    def citations(self) -> list:
        '''
        :type: :class:`list`
        '''
        return self._citations

    @property
    def embedding(self) -> dict:
        '''
        :type: :class:`dict`
        '''
        return self._embedding

    @property
    def externalIds(self) -> dict:
        '''
        :type: :class:`dict`
        '''
        return self._externalIds

    @property
    def fieldsOfStudy(self) -> list:
        '''
        :type: :class:`list`
        '''
        return self._fieldsOfStudy

    @property
    def influentialCitationCount(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._influentialCitationCount

    @property
    def isOpenAccess(self) -> bool:
        '''
        :type: :class:`bool`
        '''
        return self._isOpenAccess

    @property
    def journal(self) -> semanticscholar.Journal.Journal:
        '''
        :type: :class:`Journal`
        '''
        return self._journal

    @property
    def paperId(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._paperId

    @property
    def publicationDate(self) -> datetime:
        '''
        :type: :class:`datetime`
        '''
        return self._publicationDate

    @property
    def publicationTypes(self) -> list:
        '''
        :type: :class:`list`
        '''
        return self._publicationTypes

    @property
    def referenceCount(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._referenceCount

    @property
    def references(self) -> list:
        '''
        :type: :class:`list`
        '''
        return self._references

    @property
    def s2FieldsOfStudy(self) -> list:
        '''
        :type: :class:`list`
        '''
        return self._s2FieldsOfStudy

    @property
    def title(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._title

    @property
    def tldr(self) -> semanticscholar.Tldr.Tldr:
        '''
        :type: :class:`Tldr`
        '''
        return self._tldr

    @property
    def url(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._url

    @property
    def venue(self) -> str:
        '''
        :type: :class:`str`
        '''
        return self._venue

    @property
    def year(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._year

    @property
    def raw_data(self) -> dict:
        '''
        :type: :class:`dict`
        '''
        return self._data

    def _init_attributes(self, data) -> None:
        self._data = data
        if 'abstract' in data:
            self._abstract = data['abstract']
        if 'authors' in data:
            items = []
            for item in data['authors']:
                items.append(semanticscholar.Author.Author(item))
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
        if 'journal' in data:
            if data['journal'] is not None:
                self._journal = semanticscholar.Journal.Journal(data['journal'])
        if 'paperId' in data:
            self._paperId = data['paperId']
        if 'publicationDate' in data:
            if data['publicationDate'] is not None:
                self._publicationDate = datetime.strptime(
                    data['publicationDate'], '%Y-%m-%d')
        if 'publicationTypes' in data:
            self._publicationTypes = data['publicationTypes']
        if 'referenceCount' in data:
            self._referenceCount = data['referenceCount']
        if 'references' in data:
            items = []
            for item in data['references']:
                items.append(Paper(item))
            self._references = items
        if 's2FieldsOfStudy' in data:
            self._s2FieldsOfStudy = data['s2FieldsOfStudy']
        if 'title' in data:
            self._title = data['title']
        if 'tldr' in data:
            if data['tldr'] is not None:
                self._tldr = semanticscholar.Tldr.Tldr(data['tldr'])
        if 'url' in data:
            self._url = data['url']
        if 'venue' in data:
            self._venue = data['venue']
        if 'year' in data:
            self._year = data['year']
