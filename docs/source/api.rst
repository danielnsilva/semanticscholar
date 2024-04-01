API Endpoints
-------------

/author/batch
^^^^^^^^^^^^^

* 
	* POST: :meth:`semanticscholar.SemanticScholar.SemanticScholar.get_authors()`

/author/search
^^^^^^^^^^^^^^

* 
	* GET: :meth:`semanticscholar.SemanticScholar.SemanticScholar.search_author()`

/author/{author_id}
^^^^^^^^^^^^^^^^^^^

* 
	* GET: :meth:`semanticscholar.SemanticScholar.SemanticScholar.get_author()`

/paper/batch
^^^^^^^^^^^^

* 
	* POST: :meth:`semanticscholar.SemanticScholar.SemanticScholar.get_papers()`

/paper/search
^^^^^^^^^^^^^

* 
	* GET: :meth:`semanticscholar.SemanticScholar.SemanticScholar.search_paper()`

/paper/{author_id}
^^^^^^^^^^^^^^^^^^

* /papers
	* POST: :meth:`semanticscholar.SemanticScholar.SemanticScholar.get_author_papers()`

/paper/{paper_id}
^^^^^^^^^^^^^^^^^

* 
	* GET: :meth:`semanticscholar.SemanticScholar.SemanticScholar.get_paper()`
* /authors
	* POST: :meth:`semanticscholar.SemanticScholar.SemanticScholar.get_paper_authors()`
* /citations
	* POST: :meth:`semanticscholar.SemanticScholar.SemanticScholar.get_paper_citations()`
* /references
	* POST: :meth:`semanticscholar.SemanticScholar.SemanticScholar.get_paper_references()`

/recommendations/v1
^^^^^^^^^^^^^^^^^^^

* /papers/
	* POST: :meth:`semanticscholar.SemanticScholar.SemanticScholar.get_recommended_papers_from_lists()`
* /papers/forpaper/{paper_id}
	* GET: :meth:`semanticscholar.SemanticScholar.SemanticScholar.get_recommended_papers()`
