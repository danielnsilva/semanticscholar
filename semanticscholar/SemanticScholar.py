from time import time
import warnings
from semanticscholar.ApiRequester import ApiRequester
from semanticscholar.Author import Author
from semanticscholar.PaginatedResults import PaginatedResults
from semanticscholar.Paper import Paper


class SemanticScholar:

    DEFAULT_API_URL = 'https://api.semanticscholar.org/graph/v1'
    DEFAULT_PARTNER_API_URL = 'https://partner.semanticscholar.org/v1'

    auth_header = {}

    def __init__(
                self,
                timeout: int=2,
                api_key: str=None,
                api_url: str=None,
                graph_api: bool=True
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
            if not graph_api:
                self.api_url = self.api_url.replace('/graph', '')

        if api_key:
            self.auth_header = {'x-api-key': api_key}
            if not api_url:
                self.api_url = self.DEFAULT_PARTNER_API_URL

        self._timeout = timeout
        self._requester = ApiRequester(self._timeout)

    def get_timeout(self):
        return self._timeout

    def set_timeout(self, timeout: int):
        self._timeout = timeout
        self._requester.timeout = timeout

    timeout = property(get_timeout, set_timeout)

    def get_paper(self, id: str, include_unknown_refs: bool=False, fields: list=None) -> dict:
        '''Paper lookup

        :param str id: S2PaperId, DOI or ArXivId.
        :param float timeout: an exception is raised
            if the server has not issued a response for timeout seconds.
        :param bool include_unknown_refs:
            (optional) include non referenced paper.
        :returns: paper data or empty :class:`dict` if not found.
        :rtype: :class:`dict`
        '''

        if not fields:
            fields = Paper.FIELDS

        url = '{}/paper/{}'.format(self.api_url, id)
        
        parameters = '&fields={}'.format(','.join(fields))
        parameters += '&include_unknown_references=true' if include_unknown_refs else ''

        data = self._requester.get_data(url, parameters, self.auth_header)
        paper = Paper(data)

        return paper

    def search_paper(
                self,
                query: str,
                fields: list=None,
                limit: int=100
            ) -> PaginatedResults:
        '''Search for papers by keyword

        :param str query: plain-text search query string.
        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return
            (must be <= 100).
        :returns: query results.
        :rtype: :class:`PaginatedResults`
        '''

        if not fields:
            fields = Paper.SEARCH_FIELDS

        url = '{}/paper/search'.format(self.api_url)

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

    def get_author(self, id: str, fields: list=None) -> dict:
        '''Author lookup

        :param str id: S2AuthorId.
        :returns: author data or empty :class:`dict` if not found.
        :rtype: :class:`dict`
        '''

        if not fields:
            fields = Author.FIELDS

        url = '{}/author/{}'.format(self.api_url, id)
        
        parameters = '&fields={}'.format(','.join(fields))

        data = self._requester.get_data(url, parameters, self.auth_header)
        author = Author(data)

        return author

    def search_author(
                self,
                query: str,
                fields: list=None,
                limit: int=1000
            ) -> PaginatedResults:
        '''Search for authors by name

        :param str query: plain-text search query string.
        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return
            (must be <= 1000).
        :returns: query results.
        :rtype: :class:`PaginatedResults`
        '''

        if not fields:
            fields = Author.SEARCH_FIELDS

        url = '{}/author/search'.format(self.api_url)

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

    def paper(self, id: str, include_unknown_refs: bool=False) -> dict:
        '''Paper lookup
        :param str id: S2PaperId, DOI or ArXivId.
        :param float timeout: an exception is raised
            if the server has not issued a response for timeout seconds.
        :param bool include_unknown_refs:
            (optional) include non referenced paper.
        :returns: paper data or empty :class:`dict` if not found.
        :rtype: :class:`dict`
        '''

        warnings.warn(
            "paper() is deprecated and will be disabled in the future," +
            " use get_paper() instead.",
            DeprecationWarning)

        data = self.get_paper(id, include_unknown_refs)

        return data

    def author(self, id: str) -> dict:
        '''Author lookup
        :param str id: S2AuthorId.
        :returns: author data or empty :class:`dict` if not found.
        :rtype: :class:`dict`
        '''

        warnings.warn(
            "author() is deprecated and will be disabled in the future," +
            " use get_author() instead.",
            DeprecationWarning)

        data = self.get_author(id)

        return data
