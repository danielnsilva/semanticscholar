:tocdepth: 4

=====
Usage
=====

Basics
======

Paginated results
-----------------

Methods that return lists of items, such as papers or authors, will paginate through results, returning the list of papers or authors up to the bound limit (default value is 100). To retrieve additional pages, you can fetch them one by one or iterate through all results.

For example, iterating over all results for a paper search:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.search_paper('Computing Machinery and Intelligence')
    all_results = [item for item in results]

Pagination is handled automatically when iterating, retrieving all available items. However, if only the first batch of results is needed, you can access them directly using the `items` property of the result object, avoiding extra API calls:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.search_paper('Computing Machinery and Intelligence')
    first_page = results.items

To fetch the next page of results, use the `next_page()` method. This method appends the next batch of items to the current list, as shown in the example below:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.search_paper('Computing Machinery and Intelligence')
    results.next_page()
    first_two_pages = results.items

Asynchronous requests
---------------------

Authenticated requests
----------------------

If you have an API key, you can pass it as an argument to the main class. This will allow you to make authenticated requests.

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar(api_key='your_api_key_here')

Paper and Author
================

Paper
-----

To access paper data:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    paper = sch.get_paper('10.1093/mind/lix.236.433')

Author
------

To access author data:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    author = sch.get_author(2262347)

Retrieve multiple items at once
-------------------------------

You can fetch up to 1000 distinct papers or authors in one API call. To do that, provide a list of IDs (array of strings).

Get details for multiple papers:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    list_of_paper_ids = [
        'CorpusId:470667',
        '10.2139/ssrn.2250500',
        '0f40b1f08821e22e859c6050916cec3667778613'
    ]
    results = sch.get_papers(list_of_paper_ids)

Get details for multiple authors:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    list_of_author_ids = ['3234559', '1726629', '1711844']
    results = sch.get_authors(list_of_author_ids)

Search by keyword
-----------------

To search for papers by keyword:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.search_paper('Computing Machinery and Intelligence')

.. warning::

    From the `official documentation <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/get_graph_paper_relevance_search>`_: "Because of the subtleties of finding partial phrase matches in different parts of the document, be cautious about interpreting the total field as a count of documents containing any particular word in the query."

To search for authors by name:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.search_author('Alan M. Turing')

Query parameters for search papers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``year: str``
"""""""""""""

Restrict results to a specific publication year or a given range, following the patterns '{year}' or '{start}-{end}'. Also you can omit the start or the end. Examples: '2000', '1991-2000', '1991-', '-2000'.

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.search_paper('software engineering', year=2000)

``fields_of_study: list``
"""""""""""""""""""""""""

Restrict results to a given list of fields of study. Check `official documentation <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/get_graph_paper_relevance_search>`_ for a list of available fields.

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.search_paper('software engineering', fields_of_study=['Computer Science','Education'])

Recommended papers
==================

To get recommended papers for a given paper:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.get_recommended_papers('10.2139/ssrn.2250500')

To get recommended papers based on a list of positive and negative paper examples:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    positive_paper_ids = ['10.1145/3544585.3544600']
    negative_paper_ids = ['10.1145/301250.301271']
    results = sch.get_recommended_papers_from_lists(positive_paper_ids, negative_paper_ids)

You can also omit the list of negative paper IDs; in which case, the API will return recommended papers based on the list of positive paper IDs only.

Common query parameters
=======================

``fields: list``
----------------

The list of the fields to be returned. By default, the response includes all fields. As explained in `official documentation <https://api.semanticscholar.org/api-docs/graph>`_, fields like `papers` (author lookup and search) may result in responses bigger than the usual size and affect performance. Consider reducing the list. Check `official documentation <https://api.semanticscholar.org/api-docs/graph>`_ for a list of available fields.

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.search_paper('software engineering', fields=['title','year'])

``limit: int``
--------------

This parameter represents the maximum number of results to return on each call to API. According to `official documentation <https://api.semanticscholar.org/api-docs/graph>`_, setting a smaller limit reduces output size and latency. The default value is 100.

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.search_paper('software engineering', limit=5)

Troubleshooting
===============
