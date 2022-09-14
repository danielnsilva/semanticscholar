from semanticscholar.ApiRequester import ApiRequester
from semanticscholar.Author import Author
from semanticscholar.PaginatedList import PaginatedList
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
        
        parameters = ''
        parameters = '&fields={}'.format(','.join(fields)) if fields else ''
        parameters = '&include_unknown_references=true' if include_unknown_refs else ''

        data = self._requester.get_data(url, parameters, self.auth_header)
        paper = Paper(data)

        return paper

    def search_paper(self) -> PaginatedList:
        raise NotImplementedError

    def get_author(self, id: str, fields: list=None) -> dict:
        '''Author lookup

        :param str id: S2AuthorId.
        :returns: author data or empty :class:`dict` if not found.
        :rtype: :class:`dict`
        '''

        if not fields:
            fields = Author.FIELDS

        url = '{}/author/{}'.format(self.api_url, id)
        
        parameters = ''
        parameters = '&fields={}'.format(','.join(fields)) if fields else ''

        data = self._requester.get_data(url, parameters, self.auth_header)
        author = Author(data)

        return author

    def search_author(self) -> PaginatedList:
        raise NotImplementedError
