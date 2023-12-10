from typing import List, Literal
import asyncio
import nest_asyncio

from semanticscholar.PaginatedResults import PaginatedResults
from semanticscholar.AsyncSemanticScholar import AsyncSemanticScholar
from semanticscholar.Author import Author
from semanticscholar.Paper import Paper


class SemanticScholar():
    '''
    Main class to retrieve data from Semantic Scholar Graph API synchronously.
    '''

    def __init__(
                self,
                timeout: int = 30,
                api_key: str = None,
                api_url: str = None,
                debug: bool = False
            ) -> None:
        '''
        :param float timeout: (optional) an exception is raised\
            if the server has not issued a response for timeout seconds.
        :param str api_key: (optional) private API key.
        :param str api_url: (optional) custom API url.
        :param bool debug: (optional) enable debug mode.
        '''
        nest_asyncio.apply()
        self._timeout = timeout
        self._debug = debug
        self._AsyncSemanticScholar = AsyncSemanticScholar(
            timeout=timeout,
            api_key=api_key,
            api_url=api_url,
            debug=debug
        )

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
        self._AsyncSemanticScholar.timeout = timeout
    
    @property
    def debug(self) -> bool:
        '''
        :type: :class:`bool`
        '''
        return self._debug
    
    @debug.setter
    def debug(self, debug: bool) -> None:
        '''
        :param bool debug:
        '''
        self._debug = debug
        self._AsyncSemanticScholar.debug = debug

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

        loop = asyncio.get_event_loop()
        paper = loop.run_until_complete(
            self._AsyncSemanticScholar.get_paper(
                paper_id=paper_id, 
                fields=fields
                )
        )

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

        loop = asyncio.get_event_loop()
        papers = loop.run_until_complete(
            self._AsyncSemanticScholar.get_papers(
                paper_ids=paper_ids,
                fields=fields
                )
        )

        return papers

    def get_paper_authors(
                self,
                paper_id: str,
                fields: list = None,
                limit: int = 100
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

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            self._AsyncSemanticScholar.get_paper_authors(
                paper_id=paper_id,
                fields=fields,
                limit=limit
                )
        )

        return results

    def get_paper_citations(
                self,
                paper_id: str,
                fields: list = None,
                limit: int = 100
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

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            self._AsyncSemanticScholar.get_paper_citations(
                paper_id=paper_id,
                fields=fields,
                limit=limit
                )
        )

        return results

    def get_paper_references(
                self,
                paper_id: str,
                fields: list = None,
                limit: int = 100
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

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            self._AsyncSemanticScholar.get_paper_references(
                paper_id=paper_id,
                fields=fields,
                limit=limit
                )
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
                publication_date_or_year: str = None,
                min_citation_count: int = None,
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
        :param str publication_date_or_year: (optional) restrict results to \
               the given range of publication date in the format \
               <start_date>:<end_date>, where dates are in the format \
               YYYY-MM-DD, YYYY-MM, or YYYY.
        :param int min_citation_count: (optional) restrict results to papers \
               with at least the given number of citations.
        :param int limit: (optional) maximum number of results to return \
               (must be <= 100).
        :returns: query results.
        :rtype: :class:`semanticscholar.PaginatedResults.PaginatedResults`
        '''

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            self._AsyncSemanticScholar.search_paper(
                query=query,
                year=year,
                publication_types=publication_types,
                open_access_pdf=open_access_pdf,
                venue=venue,
                fields_of_study=fields_of_study,
                fields=fields,
                publication_date_or_year=publication_date_or_year,
                min_citation_count=min_citation_count,
                limit=limit
                )
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

        loop = asyncio.get_event_loop()
        author = loop.run_until_complete(
            self._AsyncSemanticScholar.get_author(
                author_id=author_id,
                fields=fields
                )
        )

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

        loop = asyncio.get_event_loop()
        authors = loop.run_until_complete(
            self._AsyncSemanticScholar.get_authors(
                author_ids=author_ids,
                fields=fields
                )
        )

        return authors

    def get_author_papers(
                self,
                author_id: str,
                fields: list = None,
                limit: int = 100
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

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            self._AsyncSemanticScholar.get_author_papers(
                author_id=author_id,
                fields=fields,
                limit=limit
                )
        )

        return results

    def search_author(
                self,
                query: str,
                fields: list = None,
                limit: int = 100
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

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            self._AsyncSemanticScholar.search_author(
                query=query,
                fields=fields,
                limit=limit
                )
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

        loop = asyncio.get_event_loop()
        papers = loop.run_until_complete(
            self._AsyncSemanticScholar.get_recommended_papers(
                paper_id=paper_id,
                fields=fields,
                limit=limit,
                pool_from=pool_from
                )
        )

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

        loop = asyncio.get_event_loop()
        papers = loop.run_until_complete(
            self._AsyncSemanticScholar.get_recommended_papers_from_lists(
                positive_paper_ids=positive_paper_ids,
                negative_paper_ids=negative_paper_ids,
                fields=fields,
                limit=limit
                )
        )

        return papers
