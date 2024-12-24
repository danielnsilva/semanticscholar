import logging
import re
import warnings
from typing import List, Literal, Tuple, Union

from semanticscholar.ApiRequester import ApiRequester
from semanticscholar.Author import Author
from semanticscholar.BaseReference import BaseReference
from semanticscholar.Citation import Citation
from semanticscholar.PaginatedResults import PaginatedResults
from semanticscholar.Paper import Paper
from semanticscholar.Reference import Reference
from semanticscholar.Autocomplete import Autocomplete

logger = logging.getLogger('semanticscholar')


class AsyncSemanticScholar:
    '''
    Main class to retrieve data from Semantic Scholar Graph API asynchronously.
    '''

    DEFAULT_API_URL = 'https://api.semanticscholar.org'

    BASE_PATH_GRAPH = '/graph/v1'
    BASE_PATH_RECOMMENDATIONS = '/recommendations/v1'

    auth_header = {}

    def __init__(
                self,
                timeout: int = 30,
                api_key: str = None,
                api_url: str = None,
                debug: bool = False,
                retry: bool = True,
            ) -> None:
        '''
        :param float timeout: (optional) an exception is raised
               if the server has not issued a response for timeout seconds.
        :param str api_key: (optional) private API key.
        :param str api_url: (optional) custom API url.
        :param bool debug: (optional) enable debug mode.
        :param bool retry: enable retry mode.
        '''

        if debug:
            warnings.warn(
                'The debug parameter is deprecated and will be removed in a \
                future release. Use Python\'s standard logging in DEBUG level \
                instead.')

        if api_url:
            self.api_url = api_url
        else:
            self.api_url = self.DEFAULT_API_URL

        if api_key:
            self.auth_header = {'x-api-key': api_key}

        self._timeout = timeout
        self._retry = retry
        self._requester = ApiRequester(self._timeout, self._retry)
        self.debug = debug

    @property
    def timeout(self) -> int:
        '''
        Timeout for server response in seconds.

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

    @property
    def debug(self) -> bool:
        '''
        Enable/disable debug mode.

        :type: :class:`bool`

        .. deprecated:: 0.8.4
            Use Python\'s standard logging in DEBUG level instead.
        '''
        return self._debug

    @debug.setter
    def debug(self, debug: bool) -> None:
        '''
        :param bool debug:
        '''
        self._debug = debug
        if self._debug:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.WARNING)

    @property
    def retry(self) -> bool:
        '''
        Enable/disable retry mode.

        :type: :class:`bool`
        '''
        return self._retry
    
    @retry.setter
    def retry(self, retry: bool) -> None:
        '''
        :param bool retry:
        '''
        self._retry = retry
        self._requester.retry = retry

    async def get_paper(
                self,
                paper_id: str,
                fields: list = None
            ) -> Paper:
        '''
        Paper lookup

        :calls: `GET /graph/v1/paper/{paper_id} \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data\
            /operation/get_graph_get_paper>`_

        :param str paper_id: S2PaperId, CorpusId, DOI, ArXivId, MAG, ACL, 
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

        data = await self._requester.get_data_async(url, parameters, self.auth_header)
        paper = Paper(data)

        return paper

    async def get_papers(
                self,
                paper_ids: List[str],
                fields: list = None,
                return_not_found: bool = False
            ) -> Union[List[Paper], Tuple[List[Paper], List[str]]]:
        '''
        Get details for multiple papers at once

        :calls: `POST /graph/v1/paper/batch \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data\
            /operation/post_graph_get_papers>`_

        :param str paper_ids: list of IDs (must be <= 500) - S2PaperId, 
            CorpusId, DOI, ArXivId, MAG, ACL, PMID, PMCID, or URL from:

            - semanticscholar.org
            - arxiv.org
            - aclweb.org
            - acm.org
            - biorxiv.org

        :param list fields: (optional) list of the fields to be returned.
        :param bool return_not_found: (optional) flag to include not found IDs 
               in the return, except for IDs in URL:<url> format.
        :returns: papers data, and optionally list of IDs not found.
        :rtype: :class:`List` of :class:`semanticscholar.Paper.Paper` 
                or :class:`Tuple` [:class:`List` of 
                :class:`semanticscholar.Paper.Paper`, 
                :class:`List` of :class:`str`]
        :raises: BadQueryParametersException: if no paper was found.
        '''

        if len(paper_ids) > 500 or len(paper_ids) == 0:
            raise ValueError(
                'The paper_ids parameter must be a list of 1 to 500 IDs.')

        if not fields:
            fields = Paper.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/paper/batch'

        fields = ','.join(fields)
        parameters = f'&fields={fields}'

        payload = { "ids": paper_ids }

        data = await self._requester.get_data_async(
            url, parameters, self.auth_header, payload)
        papers = [Paper(item) for item in data if item is not None]

        not_found_ids = self._get_not_found_ids(paper_ids, papers)

        if not_found_ids:
            logger.warning(f"IDs not found: {not_found_ids}")

        return papers if not return_not_found else (papers, not_found_ids)

    def _get_not_found_ids(self, paper_ids, papers):

        prefix_mapping = {
            'ARXIV': 'ArXiv',
            'MAG': 'MAG',
            'ACL': 'ACL',
            'PMID': 'PubMed',
            'PMCID': 'PubMedCentral',
            'CorpusId': 'CorpusId'
        }
        prefix_mapping = {v.lower(): k for k, v in prefix_mapping.items()}

        found_ids = set()
        for paper in papers:
            found_ids.add(paper.paperId)
            if paper.externalIds:
                for prefix, value in paper.externalIds.items():
                    if prefix.lower() in prefix_mapping:
                        found_ids.add(
                            f'{prefix_mapping[prefix.lower()]}:{value}')
                    else:
                        found_ids.add(f'{value}')
        found_ids = {id.lower() for id in found_ids}

        not_found_ids = [id for id in paper_ids if id.lower() not in found_ids]

        return not_found_ids

    async def get_paper_authors(
                self,
                paper_id: str,
                fields: list = None,
                limit: int = 100
            ) -> PaginatedResults:
        '''
        Get details about a paper's authors

        :calls: `POST /graph/v1/paper/{paper_id}/authors \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data\
            /operation/get_graph_get_paper_authors>`_

        :param str paper_id: S2PaperId, CorpusId, DOI, ArXivId, MAG, ACL, 
               PMID, PMCID, or URL from:

               - semanticscholar.org
               - arxiv.org
               - aclweb.org
               - acm.org
               - biorxiv.org

        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return 
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

        results = await PaginatedResults.create(
                requester=self._requester,
                data_type=Author,
                url=url,
                fields=fields,
                limit=limit
            )

        return results

    async def get_paper_citations(
                self,
                paper_id: str,
                fields: list = None,
                limit: int = 100
            ) -> PaginatedResults:
        '''
        Get details about a paper's citations

        :calls: `POST /graph/v1/paper/{paper_id}/citations \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data\
            /operation/get_graph_get_paper_citations>`_

        :param str paper_id: S2PaperId, CorpusId, DOI, ArXivId, MAG, ACL, 
               PMID, PMCID, or URL from:

               - semanticscholar.org
               - arxiv.org
               - aclweb.org
               - acm.org
               - biorxiv.org

        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return 
               (must be <= 1000).
        '''

        if limit < 1 or limit > 1000:
            raise ValueError(
                'The limit parameter must be between 1 and 1000 inclusive.')

        if not fields:
            fields = BaseReference.FIELDS + Paper.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/paper/{paper_id}/citations'

        results = await PaginatedResults.create(
                requester=self._requester,
                data_type=Citation,
                url=url,
                fields=fields,
                limit=limit
            )

        return results

    async def get_paper_references(
                self,
                paper_id: str,
                fields: list = None,
                limit: int = 100
            ) -> PaginatedResults:
        '''
        Get details about a paper's references

        :calls: `POST /graph/v1/paper/{paper_id}/references \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data\
            /operation/get_graph_get_paper_references>`_

        :param str paper_id: S2PaperId, CorpusId, DOI, ArXivId, MAG, ACL, 
               PMID, PMCID, or URL from:

               - semanticscholar.org
               - arxiv.org
               - aclweb.org
               - acm.org
               - biorxiv.org

        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return 
               (must be <= 1000).
        '''

        if limit < 1 or limit > 1000:
            raise ValueError(
                'The limit parameter must be between 1 and 1000 inclusive.')

        if not fields:
            fields = BaseReference.FIELDS + Paper.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/paper/{paper_id}/references'

        results = await PaginatedResults.create(
                requester=self._requester,
                data_type=Reference,
                url=url,
                fields=fields,
                limit=limit
            )

        return results

    async def search_paper(
                self,
                query: str,
                year: str = None,
                publication_types: list = None,
                open_access_pdf: bool = None,
                venue: list = None,
                fields_of_study: list = None,
                fields: list = None,
                publication_date_or_year: str = None,
                min_citation_count: int = None,
                limit: int = 100,
                bulk: bool = False,
                sort: str = None,
                match_title: bool = False
            ) -> Union[PaginatedResults, Paper]:
        '''
        Search for papers by keyword. Performs a search query based on the 
        S2 search relevance algorithm, or a bulk retrieval of basic paper 
        data without search relevance (if bulk=True). Paper relevance 
        search is the default behavior and returns up to 1,000 results. 
        Bulk retrieval instead returns up to 10,000,000 results (1,000 
        in each page).

        :calls: `GET /graph/v1/paper/search \
                <https://api.semanticscholar.org/api-docs/graph#tag/\
                Paper-Data/operation/get_graph_paper_relevance_search>`_
        :calls: `GET /graph/v1/paper/search/bulk \
                <https://api.semanticscholar.org/api-docs/graph#tag/\
                Paper-Data/operation/get_graph_paper_bulk_search>`_

        :param str query: plain-text search query string.
        :param str year: (optional) restrict results to the given range of 
               publication year.
        :param list publication_type: (optional) restrict results to the given 
               publication type list.
        :param bool open_access_pdf: (optional) restrict results to papers 
               with public PDFs.
        :param list venue: (optional) restrict results to the given venue list.
        :param list fields_of_study: (optional) restrict results to given 
               field-of-study list, using the s2FieldsOfStudy paper field.
        :param list fields: (optional) list of the fields to be returned.
        :param str publication_date_or_year: (optional) restrict results to 
               the given range of publication date in the format 
               <start_date>:<end_date>, where dates are in the format 
               YYYY-MM-DD, YYYY-MM, or YYYY.
        :param int min_citation_count: (optional) restrict results to papers 
               with at least the given number of citations.
        :param int limit: (optional) maximum number of results to return 
               (must be <= 100).
        :param bool bulk: (optional) bulk retrieval of basic paper data 
               without search relevance (ignores the limit parameter if True 
               and returns up to 1,000 results in each page).
        :param str sort: (optional) sorts results (only if bulk=True) using 
               <field>:<order> format, where "field" is either paperId, 
               publicationDate, or citationCount, and "order" is asc 
               (ascending) or desc (descending).
        :param bool match_title: (optional) retrieve a single paper whose 
               title best matches the given query.
        :returns: query results.
        :rtype: :class:`semanticscholar.PaginatedResults.PaginatedResults` or 
            :class:`semanticscholar.Paper.Paper`
        '''

        if limit < 1 or limit > 100:
            raise ValueError(
                'The limit parameter must be between 1 and 100 inclusive.')

        if not fields:
            fields = Paper.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/paper/search'
        
        if bulk:
            url += '/bulk'
            if sort:
                query += f'&sort={sort}'
        elif sort:
            warnings.warn(
                'The sort parameter is only used when bulk=True.')

        if match_title:
            url += '/match'
            if bulk:
                raise ValueError(
                    'The match_title parameter is not allowed when bulk=True.')

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

        if publication_date_or_year:
            single_date_regex = r'\d{4}(-\d{2}(-\d{2})?)?'
            full_regex = r'^({0})?(:({0})?)?$'.format(single_date_regex)
            if not bool(re.fullmatch(full_regex, publication_date_or_year)):
                raise ValueError(
                    'The publication_date_or_year parameter must be in the \
                    format <start_date>:<end_date>, where dates are in the \
                    format YYYY-MM-DD, YYYY-MM, or YYYY.')
            else:
                query += f'&publicationDateOrYear={publication_date_or_year}'

        if min_citation_count:
            query += f'&minCitationCount={min_citation_count}'
        
        max_results = 10000000 if bulk else 1000

        results = await PaginatedResults.create(
                self._requester,
                Paper,
                url,
                query,
                fields,
                limit,
                self.auth_header,
                max_results=max_results
            )

        return results if not match_title else results[0]

    async def get_author(
                self,
                author_id: str,
                fields: list = None
            ) -> Author:
        '''
        Author lookup

        :calls: `GET /graph/v1/author/{author_id} \
            <https://api.semanticscholar.org/api-docs/graph#tag/Author-Data\
            /operation/get_graph_get_author>`_

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

        data = await self._requester.get_data_async(url, parameters, self.auth_header)
        author = Author(data)

        return author

    async def get_authors(
                self,
                author_ids: List[str],
                fields: list = None,
                return_not_found: bool = False
            ) -> Union[List[Author], Tuple[List[Author], List[str]]]:
        '''
        Get details for multiple authors at once

        :calls: `POST /graph/v1/author/batch \
            <https://api.semanticscholar.org/api-docs/graph#tag/Author-Data\
            /operation/get_graph_get_author>`_

        :param str author_ids: list of S2AuthorId (must be <= 1000).
        :returns: author data, and optionally list of IDs not found.
        :rtype: :class:`List` of :class:`semanticscholar.Author.Author` 
                or :class:`Tuple` [:class:`List` of 
                :class:`semanticscholar.Author.Author`, 
                :class:`List` of :class:`str`]
        :raises: BadQueryParametersException: if no author was found.
        '''

        if len(author_ids) > 1000 or len(author_ids) == 0:
            raise ValueError(
                'The author_ids parameter must be a list of 1 to 1000 IDs.')

        if not fields:
            fields = Author.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/author/batch'

        fields = ','.join(fields)
        parameters = f'&fields={fields}'

        payload = { "ids": author_ids }

        data = await self._requester.get_data_async(
            url, parameters, self.auth_header, payload)
        authors = [Author(item) for item in data if item is not None]

        found_ids = [author.authorId for author in authors]
        not_found_ids = list(set(author_ids) - set(found_ids))

        if not_found_ids:
            logger.warning(f"IDs not found: {not_found_ids}")

        return authors if not return_not_found else (authors, not_found_ids)

    async def get_author_papers(
                self,
                author_id: str,
                fields: list = None,
                limit: int = 100
            ) -> PaginatedResults:
        '''
        Get details about a author's papers

        :calls: `POST /graph/v1/paper/{author_id}/papers \
            <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data\
            /operation/get_graph_get_author_papers>`_

        :param str paper_id: S2PaperId, CorpusId, DOI, ArXivId, MAG, ACL, 
               PMID, PMCID, or URL from:

               - semanticscholar.org
               - arxiv.org
               - aclweb.org
               - acm.org
               - biorxiv.org

        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return 
               (must be <= 1000).
        '''

        if limit < 1 or limit > 1000:
            raise ValueError(
                'The limit parameter must be between 1 and 1000 inclusive.')

        if not fields:
            fields = Paper.SEARCH_FIELDS

        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f'{base_url}/author/{author_id}/papers'

        results = await PaginatedResults.create(
                requester=self._requester,
                data_type=Paper,
                url=url,
                fields=fields,
                limit=limit
            )

        return results

    async def search_author(
                self,
                query: str,
                fields: list = None,
                limit: int = 100
            ) -> PaginatedResults:
        '''
        Search for authors by name

        :calls: `GET /graph/v1/author/search \
            <https://api.semanticscholar.org/api-docs/graph#tag/Author-Data\
            /operation/get_graph_get_author_search>`_

        :param str query: plain-text search query string.
        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of results to return 
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

        results = await PaginatedResults.create(
                self._requester,
                Author,
                url,
                query,
                fields,
                limit,
                self.auth_header,
                max_results=1000
            )

        return results

    async def get_recommended_papers(
                self,
                paper_id: str,
                fields: list = None,
                limit: int = 100,
                pool_from: Literal["recent", "all-cs"] = "recent"
            ) -> List[Paper]:
        '''
        Get recommended papers for a single positive example.

        :calls: `GET /recommendations/v1/papers/forpaper/{paper_id} \
            <https://api.semanticscholar.org/api-docs/recommendations#\
            tag/Paper-Recommendations/operation/get_papers_for_paper>`_

        :param str paper_id: S2PaperId, CorpusId, DOI, ArXivId, MAG, ACL, 
               PMID, PMCID, or URL from:

               - semanticscholar.org
               - arxiv.org
               - aclweb.org
               - acm.org
               - biorxiv.org

        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of recommendations to 
               return (must be <= 500).
        :param str pool_from: (optional) which pool of papers to recommend 
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

        data = await self._requester.get_data_async(url, parameters, self.auth_header)
        papers = [Paper(item) for item in data['recommendedPapers']]

        return papers

    async def get_recommended_papers_from_lists(
                self,
                positive_paper_ids: List[str],
                negative_paper_ids: List[str] = None,
                fields: list = None,
                limit: int = 100
            ) -> List[Paper]:
        '''
        Get recommended papers for lists of positive and negative examples.

        :calls: `POST /recommendations/v1/papers/ \
            <https://api.semanticscholar.org/api-docs/recommendations#\
            tag/Paper-Recommendations/operation/post_papers>`_

        :param list positive_paper_ids: list of paper IDs 
               that the returned papers should be related to.
        :param list negative_paper_ids: (optional) list of paper IDs 
               that the returned papers should not be related to.
        :param list fields: (optional) list of the fields to be returned.
        :param int limit: (optional) maximum number of recommendations to 
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

        data = await self._requester.get_data_async(
            url, parameters, self.auth_header, payload)
        papers = [Paper(item) for item in data['recommendedPapers']]

        return papers
    
    async def get_autocomplete(self, query: str) -> List[Autocomplete]:
        """
        Get autocomplete suggestions for a paper query.

        :calls: `GET /graph/v1/paper/autocomplete?query={query} \
            <https://api.semanticscholar.org/api-docs/graph#tag/\
            Paper-Data/operation/get_graph_get_paper_autocomplete>`_

        :param str query: query to get autocomplete suggestions for.
        :returns: list of autocomplete suggestions.
        :rtype: :class:`List` of 
                :class:`semanticscholar.Autocomplete.Autocomplete`
        """
        
        base_url = self.api_url + self.BASE_PATH_GRAPH
        url = f"{base_url}/paper/autocomplete"

        parameters = f"query={query}"

        data = await self._requester.get_data_async(
            url, parameters, self.auth_header)

        if not data or "matches" not in data:
            return []

        return [Autocomplete(suggestion) for suggestion in data["matches"]]
