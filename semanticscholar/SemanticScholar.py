from typing import List, Literal

from semanticscholar.ApiRequester import ApiRequester
from semanticscholar.Author import Author
from semanticscholar.BaseReference import BaseReference
from semanticscholar.Citation import Citation
from semanticscholar.PaginatedResults import PaginatedResults
from semanticscholar.Paper import Paper
from semanticscholar.Reference import Reference


class SemanticScholar:
    '''
    Main class to retrieve data from Semantic Scholar Graph API
    '''

    DEFAULT_API_URL = 'https://api.semanticscholar.org'
    DEFAULT_PARTNER_API_URL = 'https://partner.semanticscholar.org'

    BASE_PATH_GRAPH = '/graph/v1'
    BASE_PATH_RECOMMENDATIONS = '/recommendations/v1'

    auth_header = {}

    def __init__(
                self,
                timeout: int = 10,
                api_key: str = None,
                api_url: str = None
            ) -> None:
        '''
        :param float timeout: (optional) an exception is raised\
            if the server has not issued a response for timeout seconds.
        :param str api_key: (optional) private API key.
        :param str api_url: (optional) custom API url.
        '''

        if api_url:
            self.api_url = api_url
        else:
            self.api_url = self.DEFAULT_API_URL

        if api_key:
            self.auth_header = {'x-api-key': api_key}
            if not api_url:
                self.api_url = self.DEFAULT_PARTNER_API_URL

        self._timeout = timeout
        self._requester = ApiRequester(self._timeout)

    @property
    def timeout(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._timeout

    @timeout.setter
    def timeout(self, timeout: int) -> None:
        '''
        :param int timeout:
        '''
        self._timeout = timeout
        self._requester.timeout = timeout

    def get_paper(
                self,
                paper_id: str,
                fields: list = None
            ) -> Paper:
        '''Paper lookup

        :calls: `GET /paper/{paper_id} <https://api.semanticscholar.org/\
            api-docs/graph#tag/Paper-Data/operation/get_graph_get_paper>`_

        :param str paper_id: S2PaperId, CorpusId, DOI, ArXivId, MAG, ACL, \
               PMID, PMCID, or URL from:

               - semanticscholar.org
               - arxiv.org
               - aclweb.org
               - acm.org
               - biorxiv.org

        :param list fields: (optional) list of the fields to be returned.
        :returns: paper data
        :rtype: :class:`semanticscholar.Paper.Paper`
        :raises: ObjectNotFoundException: if Paper ID not found.
        '''

        if not fields:
            fields = Paper.FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/paper/{paper_id}'

        fields = ','.join(fields)
        parameters = f'&fields={fields}'

        data = self._requester.get_data(url, parameters, self.auth_header)
        paper = Paper(data)

        return paper

    def get_papers(
                self,
                paper_ids: List[str],
                fields: list = None
            ) -> List[Paper]:
        '''Get details for multiple papers at once

        :calls: `POST /paper/batch <https://api.semanticscholar.org/api-docs/\
            graph#tag/Paper-Data/operation/post_graph_get_papers>`_

        :param str paper_ids: list of IDs (must be <= 1000) - S2PaperId,\
            CorpusId, DOI, ArXivId, MAG, ACL, PMID, PMCID, or URL from:

            - semanticscholar.org
            - arxiv.org
            - aclweb.org
            - acm.org
            - biorxiv.org

        :param list fields: (optional) list of the fields to be returned.
        :returns: papers data
        :rtype: :class:`List` of :class:`semanticscholar.Paper.Paper`
        :raises: BadQueryParametersException: if no paper was found.
        '''

        if not fields:
            fields = Paper.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/paper/batch'

        fields = ','.join(fields)
        parameters = f'&fields={fields}'

        payload = { "ids": paper_ids }

        data = self._requester.get_data(
            url, parameters, self.auth_header, payload)
        papers = [Paper(item) for item in data]

        return papers

    def get_paper_authors(
                self,
                paper_id: str,
                fields: list = None,
                limit: int = 1000
            ) -> PaginatedResults:
        '''Get details about a paper's authors

        :calls: `POST /paper/{paper_id}/authors \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data\
            /operation/get_graph_get_paper_authors>`_

        :param str paper_id: S2PaperId, CorpusId, DOI, ArXivId, MAG, ACL,\
               PMID, PMCID, or URL from:

               - semanticscholar.org
               - arxiv.org
               - aclweb.org
               - acm.org
               - biorxiv.org

        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return\
               (must be <= 1000).
        '''

        if limit < 1 or limit > 1000:
            raise ValueError(
                'The limit parameter must be between 1 and 1000 inclusive.')

        if not fields:
            fields = [item for item in Author.SEARCH_FIELDS
                      if not item.startswith('papers')]

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/paper/{paper_id}/authors'

        results = PaginatedResults(
                requester=self._requester,
                data_type=Author,
                url=url,
                fields=fields,
                limit=limit
            )

        return results

    def get_paper_citations(
                self,
                paper_id: str,
                fields: list = None,
                limit: int = 1000
            ) -> PaginatedResults:
        '''Get details about a paper's citations

        :calls: `POST /paper/{paper_id}/citations \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data\
            /operation/get_graph_get_paper_citations>`_

        :param str paper_id: S2PaperId, CorpusId, DOI, ArXivId, MAG, ACL,\
               PMID, PMCID, or URL from:

               - semanticscholar.org
               - arxiv.org
               - aclweb.org
               - acm.org
               - biorxiv.org

        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return\
               (must be <= 1000).
        '''

        if limit < 1 or limit > 1000:
            raise ValueError(
                'The limit parameter must be between 1 and 1000 inclusive.')

        if not fields:
            fields = BaseReference.FIELDS + Paper.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/paper/{paper_id}/citations'

        results = PaginatedResults(
                requester=self._requester,
                data_type=Citation,
                url=url,
                fields=fields,
                limit=limit
            )

        return results

    def get_paper_references(
                self,
                paper_id: str,
                fields: list = None,
                limit: int = 1000
            ) -> PaginatedResults:
        '''Get details about a paper's references

        :calls: `POST /paper/{paper_id}/references \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data\
            /operation/get_graph_get_paper_references>`_

        :param str paper_id: S2PaperId, CorpusId, DOI, ArXivId, MAG, ACL,\
               PMID, PMCID, or URL from:

               - semanticscholar.org
               - arxiv.org
               - aclweb.org
               - acm.org
               - biorxiv.org

        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return\
               (must be <= 1000).
        '''

        if limit < 1 or limit > 1000:
            raise ValueError(
                'The limit parameter must be between 1 and 1000 inclusive.')

        if not fields:
            fields = BaseReference.FIELDS + Paper.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/paper/{paper_id}/references'

        results = PaginatedResults(
                requester=self._requester,
                data_type=Reference,
                url=url,
                fields=fields,
                limit=limit
            )

        return results

    def search_paper(
                self,
                query: str,
                year: str = None,
                publication_types: list = None,
                open_access_pdf: bool = None,
                venue: list = None,
                fields_of_study: list = None,
                fields: list = None,
                limit: int = 100
            ) -> PaginatedResults:
        '''Search for papers by keyword

        :calls: `GET /paper/search <https://api.semanticscholar.org/api-docs/\
            graph#tag/Paper-Data/operation/get_graph_get_paper_search>`_

        :param str query: plain-text search query string.
        :param str year: (optional) restrict results to the given range of \
               publication year.
        :param list publication_type: (optional) restrict results to the given \
               publication type list.
        :param bool open_access_pdf: (optional) restrict results to papers \
               with public PDFs.
        :param list venue: (optional) restrict results to the given venue list.
        :param list fields_of_study: (optional) restrict results to given \
               field-of-study list, using the s2FieldsOfStudy paper field.
        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return \
               (must be <= 100).
        :returns: query results.
        :rtype: :class:`semanticscholar.PaginatedResults.PaginatedResults`
        '''

        if limit < 1 or limit > 100:
            raise ValueError(
                'The limit parameter must be between 1 and 100 inclusive.')

        if not fields:
            fields = Paper.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/paper/search'

        query += f'&year={year}' if year else ''

        if publication_types:
            publication_types = ','.join(publication_types)
            query += f'&publicationTypes={publication_types}'

        query += '&openAccessPdf' if open_access_pdf else ''

        if venue:
            venue = ','.join(venue)
            query += f'&venue={venue}'

        if fields_of_study:
            fields_of_study = ','.join(fields_of_study)
            query += f'&fieldsOfStudy={fields_of_study}'

        results = PaginatedResults(
                self._requester,
                Paper,
                url,
                query,
                fields,
                limit,
                self.auth_header
            )

        return results

    def get_author(
                self,
                author_id: str,
                fields: list = None
            ) -> Author:
        '''Author lookup

        :calls: `GET /author/{author_id} <https://api.semanticscholar.org/\
            api-docs/graph#tag/Author-Data/operation/get_graph_get_author>`_

        :param str author_id: S2AuthorId.
        :returns: author data
        :rtype: :class:`semanticscholar.Author.Author`
        :raises: ObjectNotFoundException: if Author ID not found.
        '''

        if not fields:
            fields = Author.FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/author/{author_id}'

        fields = ','.join(fields)
        parameters = f'&fields={fields}'

        data = self._requester.get_data(url, parameters, self.auth_header)
        author = Author(data)

        return author

    def get_authors(
                self,
                author_ids: List[str],
                fields: list = None
            ) -> List[Author]:
        '''Get details for multiple authors at once

        :calls: `POST /author/batch <https://api.semanticscholar.org/api-docs/\
            graph#tag/Author-Data/operation/get_graph_get_author>`_

        :param str author_ids: list of S2AuthorId (must be <= 1000).
        :returns: author data
        :rtype: :class:`List` of :class:`semanticscholar.Author.Author`
        :raises: BadQueryParametersException: if no author was found.
        '''

        if not fields:
            fields = Author.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/author/batch'

        fields = ','.join(fields)
        parameters = f'&fields={fields}'

        payload = { "ids": author_ids }

        data = self._requester.get_data(
            url, parameters, self.auth_header, payload)
        authors = [Author(item) for item in data]

        return authors

    def get_author_papers(
                self,
                author_id: str,
                fields: list = None,
                limit: int = 1000
            ) -> PaginatedResults:
        '''Get details about a author's papers

        :calls: `POST /paper/{author_id}/papers \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data\
            /operation/get_graph_get_author_papers>`_

        :param str paper_id: S2PaperId, CorpusId, DOI, ArXivId, MAG, ACL,\
               PMID, PMCID, or URL from:

               - semanticscholar.org
               - arxiv.org
               - aclweb.org
               - acm.org
               - biorxiv.org

        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return\
               (must be <= 1000).
        '''

        if limit < 1 or limit > 1000:
            raise ValueError(
                'The limit parameter must be between 1 and 1000 inclusive.')

        if not fields:
            fields = Paper.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/author/{author_id}/papers'

        results = PaginatedResults(
                requester=self._requester,
                data_type=Paper,
                url=url,
                fields=fields,
                limit=limit
            )

        return results

    def search_author(
                self,
                query: str,
                fields: list = None,
                limit: int = 1000
            ) -> PaginatedResults:
        '''Search for authors by name

        :calls: `GET /author/search <https://api.semanticscholar.org/api-docs/\
            graph#tag/Author-Data/operation/get_graph_get_author_search>`_

        :param str query: plain-text search query string.
        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return \
               (must be <= 1000).
        :returns: query results.
        :rtype: :class:`semanticscholar.PaginatedResults.PaginatedResults`
        '''

        if limit < 1 or limit > 1000:
            raise ValueError(
                'The limit parameter must be between 1 and 1000 inclusive.')

        if not fields:
            fields = Author.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/author/search'

        results = PaginatedResults(
                self._requester,
                Author,
                url,
                query,
                fields,
                limit,
                self.auth_header
            )

        return results

    def get_recommended_papers(
                self,
                paper_id: str,
                fields: list = None,
                limit: int = 100,
                pool_from: Literal["recent", "all-cs"] = "recent"
            ) -> List[Paper]:
        '''Get recommended papers for a single positive example.

        :calls: `GET /recommendations/v1/papers/forpaper/{paper_id} \
            <https://api.semanticscholar.org/api-docs/recommendations#\
            tag/Paper-Recommendations/operation/get_papers_for_paper>`_

        :param str paper_id: S2PaperId, CorpusId, DOI, ArXivId, MAG, ACL,\
               PMID, PMCID, or URL from:

               - semanticscholar.org
               - arxiv.org
               - aclweb.org
               - acm.org
               - biorxiv.org

        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of recommendations to \
            return (must be <= 500).
        :param str pool_from: (optional) which pool of papers to recommend \
            from. Must be either "recent" or "all-cs".
        :returns: list of recommendations.
        :rtype: :class:`List` of :class:`semanticscholar.Paper.Paper`
        '''

        if pool_from not in ["recent", "all-cs"]:
            raise ValueError(
                'The pool_from parameter must be either "recent" or "all-cs".')

        if limit < 1 or limit > 500:
            raise ValueError(
                'The limit parameter must be between 1 and 500 inclusive.')

        if not fields:
            fields = Paper.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_RECOMMENDATIONS
        url = f'{base_url}/papers/forpaper/{paper_id}'

        fields = ','.join(fields)
        parameters = f'&fields={fields}&limit={limit}&from={pool_from}'

        data = self._requester.get_data(url, parameters, self.auth_header)
        papers = [Paper(item) for item in data['recommendedPapers']]

        return papers

    def get_recommended_papers_from_lists(
                self,
                positive_paper_ids: List[str],
                negative_paper_ids: List[str] = None,
                fields: list = None,
                limit: int = 100
            ) -> List[Paper]:
        '''Get recommended papers for lists of positive and negative examples.

        :calls: `POST /recommendations/v1/papers/ \
            <https://api.semanticscholar.org/api-docs/recommendations#\
            tag/Paper-Recommendations/operation/post_papers>`_

        :param list positive_paper_ids: list of paper IDs \
            that the returned papers should be related to.
        :param list negative_paper_ids: (optional) list of paper IDs \
            that the returned papers should not be related to.
        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of recommendations to \
            return (must be <= 500).
        :returns: list of recommendations.
        :rtype: :class:`List` of :class:`semanticscholar.Paper.Paper`
        '''

        if limit < 1 or limit > 500:
            raise ValueError(
                'The limit parameter must be between 1 and 500 inclusive.')

        if not fields:
            fields = Paper.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_RECOMMENDATIONS
        url = f'{base_url}/papers/'

        fields = ','.join(fields)
        parameters = f'&fields={fields}&limit={limit}'

        payload = {
            "positivePaperIds": positive_paper_ids,
            "negativePaperIds": negative_paper_ids
        }

        data = self._requester.get_data(
            url, parameters, self.auth_header, payload)
        papers = [Paper(item) for item in data['recommendedPapers']]

        return papers
