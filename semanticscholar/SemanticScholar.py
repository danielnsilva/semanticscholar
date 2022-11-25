import warnings

from semanticscholar.ApiRequester import ApiRequester
from semanticscholar.Author import Author
from semanticscholar.PaginatedResults import PaginatedResults
from semanticscholar.Paper import Paper


class SemanticScholar:
    '''
    Main class to retrieve data from Semantic Scholar Graph API
    '''

    DEFAULT_API_URL = 'https://api.semanticscholar.org/graph/v1'
    DEFAULT_PARTNER_API_URL = 'https://partner.semanticscholar.org/graph/v1'

    auth_header = {}

    def __init__(
                self,
                timeout: int = 10,
                api_key: str = None,
                api_url: str = None,
                graph_api: bool = True
            ) -> None:
        '''
        :param float timeout: (optional) an exception is raised
        if the server has not issued a response for timeout seconds.
        :param str api_key: (optional) private API key.
        :param str api_url: (optional) custom API url.
        :param bool graph_api: (optional) whether use new Graph API.
        '''

        if api_url:
            self.api_url = api_url
        else:
            self.api_url = self.DEFAULT_API_URL

        if api_key:
            self.auth_header = {'x-api-key': api_key}
            if not api_url:
                self.api_url = self.DEFAULT_PARTNER_API_URL
        
        if not graph_api:
            self.api_url = self.api_url.replace('/graph', '')

        self._timeout = timeout
        self._requester = ApiRequester(self._timeout)

    def get_timeout(self) -> int:
        '''
        :type: :class:`int`
        '''
        return self._timeout

    def set_timeout(self, timeout: int):
        '''
        :param int timeout:
        '''
        self._timeout = timeout
        self._requester.timeout = timeout

    timeout = property(get_timeout, set_timeout)

    def get_paper(
                self,
                paper_id: str,
                include_unknown_refs: bool = False,
                fields: list = None
            ) -> Paper:
        '''Paper lookup

        :calls: `GET https://api.semanticscholar.org/graph/v1/paper/{paper_id} \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/ \
            operation/get_graph_get_paper>`_

        :param str paper_id: S2PaperId, CorpusId, DOI, ArXivId, MAG, ACL, \
               PMID, PMCID, or URL from:

               - semanticscholar.org
               - arxiv.org
               - aclweb.org
               - acm.org
               - biorxiv.org
               
        :param bool include_unknown_refs: (optional) include non referenced \
               paper.
        :param list fields: (optional) list of the fields to be returned.
        :returns: paper data or empty :class:`dict` if not found.
        :rtype: :class:`dict`
        '''

        if not fields:
            fields = Paper.FIELDS

        url = f'{self.api_url}/paper/{paper_id}'

        fields = ','.join(fields)
        parameters = f'&fields={fields}'
        if include_unknown_refs:
            parameters += '&include_unknown_references=true'

        data = self._requester.get_data(url, parameters, self.auth_header)
        paper = Paper(data)

        return paper

    def search_paper(
                self,
                query: str,
                year: str = None,
                fields_of_study: list = None,
                fields: list = None,
                limit: int = 100
            ) -> PaginatedResults:
        '''Search for papers by keyword

        :calls: `GET https://api.semanticscholar.org/graph/v1/paper/search \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/ \
            operation/get_graph_get_paper_search>`_

        :param str query: plain-text search query string.
        :param str year: restrict results to the given range of \
               publication year.
        :param str fields_of_study: restrict results to given field-of-study, \
               using the s2FieldsOfStudy paper field.
        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return \
               (must be <= 100).
        :returns: query results.
        :rtype: :class:`PaginatedResults`
        '''

        if not fields:
            fields = Paper.SEARCH_FIELDS

        url = f'{self.api_url}/paper/search'

        query += f'&year={year}' if year else ''
        if fields_of_study:
            fields_of_study = ','.join(fields_of_study)
            query += f'&fields_of_study={fields_of_study}'

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

    def get_author(self, author_id: str, fields: list = None) -> Author:
        '''Author lookup

        :calls: `GET https://api.semanticscholar.org/graph/v1/author/\
            {author_id} <https://api.semanticscholar.org/api-docs/\
            graph#tag/Author-Data/operation/get_graph_get_author>`_

        :param str author_id: S2AuthorId.
        :returns: author data or empty :class:`dict` if not found.
        :rtype: :class:`dict`
        '''

        if not fields:
            fields = Author.FIELDS

        url = f'{self.api_url}/author/{author_id}'

        fields = ','.join(fields)
        parameters = f'&fields={fields}'

        data = self._requester.get_data(url, parameters, self.auth_header)
        author = Author(data)

        return author

    def search_author(
                self,
                query: str,
                fields: list = None,
                limit: int = 1000
            ) -> PaginatedResults:
        '''Search for authors by name

        :calls: `GET https://api.semanticscholar.org/graph/v1/author/search\
            <https://api.semanticscholar.org/api-docs/graph#tag/Author-Data/\
            operation/get_graph_get_author_search>`_

        :param str query: plain-text search query string.
        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return \
               (must be <= 1000).
        :returns: query results.
        :rtype: :class:`PaginatedResults`
        '''

        if not fields:
            fields = Author.SEARCH_FIELDS

        url = f'{self.api_url}/author/search'

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

    def paper(self, paper_id: str, include_unknown_refs: bool = False) -> dict:
        '''Paper lookup

        :calls: `GET https://api.semanticscholar.org/graph/v1/paper/{paper_id} \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/ \
            operation/get_graph_get_paper>`_

        :param str paper_id: S2PaperId, DOI or ArXivId.
        :param float timeout: an exception is raised \
               if the server has not issued a response for timeout seconds.
        :param bool include_unknown_refs: (optional) include non \
               referenced paper.
        :returns: paper data or empty :class:`dict` if not found.
        :rtype: :class:`dict`

        .. deprecated:: 0.3.0
           Use :func:`get_paper` instead
        '''

        warnings.warn(
            "paper() is deprecated and will be disabled in the future," +
            " use get_paper() instead.",
            DeprecationWarning)

        data = self.get_paper(paper_id, include_unknown_refs)

        return data.raw_data

    def author(self, paper_id: str) -> dict:
        '''Author lookup

        :calls: `GET https://api.semanticscholar.org/graph/v1/author/\
            {author_id} <https://api.semanticscholar.org/api-docs/\
            graph#tag/Author-Data/operation/get_graph_get_author>`_

        :param str paper_id: S2AuthorId.
        :returns: author data or empty :class:`dict` if not found.
        :rtype: :class:`dict`

        .. deprecated:: 0.3.0
           Use :func:`get_author` instead
        '''

        warnings.warn(
            "author() is deprecated and will be disabled in the future," +
            " use get_author() instead.",
            DeprecationWarning)

        data = self.get_author(paper_id)

        return data.raw_data
