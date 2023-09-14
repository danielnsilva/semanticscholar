from typing import List
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
        nest_asyncio.apply()
        self._timeout = timeout
        self._AsyncSemanticScholar = AsyncSemanticScholar(
            timeout=timeout,
            api_key=api_key,
            api_url=api_url
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

    def get_paper(
                self,
                *args,
                **kwargs
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
            self._AsyncSemanticScholar.get_paper(*args, **kwargs)
        )

        return paper

    def get_papers(
                self,
                *args,
                **kwargs
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
            self._AsyncSemanticScholar.get_papers(*args, **kwargs)
        )

        return papers

    def get_paper_authors(
                self,
                *args,
                **kwargs
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
            self._AsyncSemanticScholar.get_paper_authors(*args, **kwargs)
        )

        return results

    def get_paper_citations(
                self,
                *args,
                **kwargs
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
            self._AsyncSemanticScholar.get_paper_citations(*args, **kwargs)
        )

        return results

    def get_paper_references(
                self,
                *args,
                **kwargs,
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
            self._AsyncSemanticScholar.get_paper_references(*args, **kwargs)
        )

        return results

    def search_paper(
                self,
                *args,
                **kwargs
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

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(
            self._AsyncSemanticScholar.search_paper(*args, **kwargs)
        )

        return results

    def get_author(
                self,
                *args,
                **kwargs
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
            self._AsyncSemanticScholar.get_author(*args, **kwargs)
        )

        return author

    def get_authors(
                self,
                *args,
                **kwargs
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
            self._AsyncSemanticScholar.get_authors(*args, **kwargs)
        )

        return authors

    def get_author_papers(
                self,
                *args,
                **kwargs
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
            self._AsyncSemanticScholar.get_author_papers(*args, **kwargs)
        )

        return results

    def search_author(
                self,
                *args,
                **kwargs
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
            self._AsyncSemanticScholar.search_author(*args, **kwargs)
        )

        return results

    def get_recommended_papers(
                self,
                *args,
                **kwargs
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
            self._AsyncSemanticScholar.get_recommended_papers(*args, **kwargs)
        )

        return papers

    def get_recommended_papers_from_lists(
                self,
                *args,
                **kwargs
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
            self._AsyncSemanticScholar.get_recommended_papers_from_lists(*args, **kwargs)
        )

        return papers
