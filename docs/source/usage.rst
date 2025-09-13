:tocdepth: 4

=====
Usage
=====

Basics
======

Basic usage involves initializing the main class, calling one of its methods to retrieve data, and accessing the response attributes. For example, to get a paper by its ID:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    paper = sch.get_paper('10.1093/mind/lix.236.433')
    print(paper.title)

Typed responses
---------------

The library offers typed responses. This simplifies data extraction and enhances code readability. For example, to access the title of a paper:

.. code-block:: python

    paper = sch.get_paper('10.1093/mind/lix.236.433')
    print(paper.title)

You can also access the API response in its original JSON format as a dictionary. To retrieve the raw JSON data, use the ``raw_data`` attribute of the response object:

.. code-block:: python

    paper = sch.get_paper('10.1093/mind/lix.236.433')
    print(paper.raw_data)

To explore all available fields in the response, use the ``keys()`` method:

.. code-block:: python

    paper = sch.get_paper('10.1093/mind/lix.236.433')
    print(paper.keys())

.. seealso::

    Refer to the :doc:`s2objects` section for details on all available response types and their attributes.

Asynchronous requests
---------------------

The library supports both synchronous and asynchronous versions for its methods, allowing you to choose the approach that best suits your workflow.

You can use the asynchronous version with the :doc:`mainclasses/asyncsemanticscholar` class:

.. code-block:: python

    import asyncio
    from semanticscholar import AsyncSemanticScholar

    def fetch_paper():
        async def get_paper():
            sch = AsyncSemanticScholar()
            return await sch.get_paper('10.1093/mind/lix.236.433')
        return asyncio.run(get_paper())

    paper = fetch_paper()

.. _authenticated-requests:

Authenticated requests
----------------------

If you have an API key, you can pass it as an argument to the main class. This will allow you to make authenticated requests.

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar(api_key='your_api_key_here')

Retry mode
----------

The library provides an automatic retry mechanism to handle rate-limiting responses from the Semantic Scholar API.

By default, the retry mechanism is enabled (``retry=True``). When enabled, the library will automatically retry requests up to 10 times if it encounters an HTTP 429 status (`Too Many Requests`). Each retry attempt waits 30 seconds before trying again.

This feature is especially useful for handling temporary rate limits imposed by the Semantic Scholar API, ensuring your requests are eventually processed without manual intervention. If you prefer to manage retries yourself, you can disable this feature as shown below:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar(retry=False)

Response timeout
----------------

You can set the wait time for a response. By default, requests to the API will wait for 30 seconds until a ``TimeoutException`` is raised. To change the default value, specify it during the creation of a ``SemanticScholar`` instance:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar(timeout=5)

Alternatively, you can set the ``timeout`` property value:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    sch.timeout = 5

Paper and Author
================

Paper
-----

To access paper data:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    paper = sch.get_paper('10.1093/mind/lix.236.433')

For details on supported ID types, refer to the `official API documentation <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/get_graph_get_paper>`_.

Autocomplete suggestions
^^^^^^^^^^^^^^^^^^^^^^^^

Use the autocomplete feature to get suggestions for paper queries. For example:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    suggestions = sch.get_autocomplete('softw')

The response contains a list of suggestions based on the provided partial query. Each suggestion is represented by an :doc:`s2objects/Autocomplete` object, which provides minimal information about the papers. Note that these are not full :doc:`s2objects/Paper` objects with all attributes.

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

Paper Bulk retrieval
^^^^^^^^^^^^^^^^^^^^

The bulk retrieval method allows fetching up to 1,000 basic paper records per request and up 10,000,000 papers in total. This useful To retrieve a large number of papers, once ``search_paper()`` by default are limited to 1,000 results in total.

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    response = sch.search_paper(query='deep learning', bulk=True)

The query supports advanced syntax for refined searches. For details about query syntax and additional parameters, refer to the `official API documentation <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/get_graph_paper_bulk_search>`_.

.. code-block:: python

    # Search for papers containing 'deep' or 'learning'
    response = sch.search_paper(query='deep | learning', bulk=True)

Additionally, the ``sort`` parameter allows ordering results when using ``bulk=True``. Use the format ``<field>:<order>``, where:
- **field**: Can be ``paperId``, ``publicationDate``, or ``citationCount``.
- **order**: Can be ``asc`` (ascending) or ``desc`` (descending).

By default, results are sorted by ``paperId:asc``.

.. code-block:: python

    # Retrieve highly-cited papers first
    response = sch.search_paper(query='deep learning', bulk=True, sort='citationCount:desc')

Search papers by title
^^^^^^^^^^^^^^^^^^^^^^

Retrieve a single paper whose title best matches the given query.

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    paper = sch.search_paper(query='deep learning', match_title=True)

.. note::

    The ``match_title`` parameter is not compatible with the ``bulk`` parameter.

Query parameters for search papers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``year: str``
"""""""""""""

Restrict results to a specific publication year or a given range, following the patterns '{year}' or '{start}-{end}'. Also you can omit the start or the end. Examples: '2000', '1991-2000', '1991-', '-2000'.

.. code-block:: python

    results = sch.search_paper('turing test', year=2000)

``publication_type: list``
""""""""""""""""""""""""""

Restrict results to a given list of publication types. Check `official documentation <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/get_graph_paper_relevance_search>`_ for a list of available publication types.

.. code-block:: python

    results = sch.search_paper('turing test', publication_type=['Journal','Conference'])

``open_access_pdf: bool``
"""""""""""""""""""""""""

Restrict results to papers with open access PDFs. By default, this parameter is set to ``False``.

.. code-block:: python

    results = sch.search_paper('turing test', open_access_pdf=True)

``venue: list``
"""""""""""""""

Restrict results to a given list of venues.

.. code-block:: python

    results = sch.search_paper('turing test', venue=['ESEM','ICSE','ICSME'])

``fields_of_study: list``
"""""""""""""""""""""""""

Restrict results to a given list of fields of study. Check `official documentation <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/get_graph_paper_relevance_search>`_ for a list of available fields.

.. code-block:: python

    results = sch.search_paper('turing test', fields_of_study=['Computer Science','Education'])

``publication_date_or_year: str``
"""""""""""""""""""""""""""""""""

Restrict results to the given range of publication date in the format <start_date>:<end_date>, where dates are in the format YYYY-MM-DD, YYYY-MM, or YYYY.

.. code-block:: python

    results = sch.search_paper('turing test', publication_date_or_year='2020-01-01:2021-12-31')

``min_citation_count: int``
"""""""""""""""""""""""""""

Restrict results to papers with at least the given number of citations.

.. code-block:: python

    results = sch.search_paper('turing test', min_citation_count=100)

Paginated results
-----------------

Methods that return large amounts of data in chunks, such as searching for papers or authors, support pagination. These methods retrieve results up to a defined limit per page (default is 100). To access additional pages, you can fetch them individually or iterate through the entire set of results.

For example, iterating over all results for a paper search:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.search_paper('Computing Machinery and Intelligence')
    all_results = [item for item in results]

Pagination is handled automatically when iterating, retrieving all available items. However, if only the first batch of results is needed, you can access them directly using the `items` property of the result object, avoiding extra API calls:

.. code-block:: python

    results = sch.search_paper('Computing Machinery and Intelligence')
    first_page = results.items

To fetch the next page of results, use the `next_page()` method. This method appends the next batch of items to the current list, as shown in the example below:

.. code-block:: python

    results = sch.search_paper('Computing Machinery and Intelligence')
    results.next_page()
    first_two_pages = results.items

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

Datasets API
============

The Datasets API includes several key concepts:

- **Releases**: Datasets are organized into releases, which are snapshots of the data at specific points in time (e.g., '2023-12-01').
- **Datasets**: Each release contains multiple datasets, such as 'papers', 'authors', 'publications', etc.
- **Incremental Updates**: For efficient updates, the API provides diffs between releases showing only the changes.

Available releases
------------------

The response contains a list of release identifiers (strings) that you can use to access specific releases. To get a list of all available dataset releases:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    releases = sch.get_available_releases()
    print(releases)

    # Example output:
    # ['2025-08-19', '2025-09-05, ...']

Get a specific release
----------------------

To get detailed information about a specific release, including all available datasets:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    release = sch.get_release('2025-08-19')
    
    print(f"Release ID: {release.release_id}")
    print(f"Number of datasets: {len(release.datasets)}")
    
    # List all available datasets in this release
    for dataset in release.datasets:
        print(f"- {dataset.name}: {dataset.description}")

Per `the official documentation <https://api.semanticscholar.org/api-docs/datasets#tag/Datasets/operation/get_release>`_, you can also use 'latest' as the release identifier to get the most recent release.

Get dataset download links
--------------------------

This endpoint requires :ref:`authentication <authenticated-requests>` with a valid API key. To get download links for a specific dataset in a release:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    dataset = sch.get_dataset_download_links('2025-08-19', 'papers')
    
    print(f"Dataset: {dataset.name}")
    print(f"Description: {dataset.description}")
    print(f"Number of files: {len(dataset.files)}")
    
    # Print first few download URLs
    for i, file_url in enumerate(dataset.files[:3]):
        print(f"File {i+1}: {file_url}")

Get dataset diffs
-----------------

This endpoint requires :ref:`authentication <authenticated-requests>` with a valid API key. To get file urls for incremental updates between two releases for a specific dataset:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    diffs = sch.get_dataset_diffs('papers', '2023-12-01', '2024-01-01')
    
    print(f"Number of incremental updates: {len(diffs.diffs)}")
    
    # Examine the first diff
    first_diff = diffs.diffs[0]
    print(f"First update: {first_diff.from_release} -> {first_diff.to_release}")
    print(f"Update files: {len(first_diff.update_files)}")
    print(f"Delete files: {len(first_diff.delete_files)}")

Actually using the diffs to update your local dataset is not supported by this library. Please see the official
`documentation <https://api.semanticscholar.org/api-docs/datasets#tag/Incremental-Updates/operation/get_diff>`_ for an example using Spark.

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

If you encounter issues while using the ``semanticscholar`` library, enabling debug-level logging can provide valuable insights into the underlying HTTP requests and responses. This can help you identify the root cause of the problem and resolve it more efficiently.

Enabling debug logging
----------------------

You can enable debug-level logging globally or just for the ``semanticscholar`` library.

1. **Enable debug logging globally**:
    
.. code-block:: python

    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    
This will enable debug-level logging for all loggers, including the ``semanticscholar`` library, its dependencies, and any other libraries you are using. While these messages may not be directly related, they can still provide valuable context for identifying related issues or understanding broader behavior.


2. **Enable debug logging for the semanticscholar library only**:

.. code-block:: python

    import logging
    logging.getLogger('semanticscholar').setLevel(logging.DEBUG)
    
This restricts debug-level logging to the ``semanticscholar`` library.

In both cases, the output will include detailed information about HTTP requests, headers, payloads, and the equivalent ``curl`` command. For example:

.. code-block::

    DEBUG:semanticscholar:HTTP Request: POST https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,year
    DEBUG:semanticscholar:Headers: {'x-api-key': 'F@k3K3y'}
    DEBUG:semanticscholar:Payload: {'ids': ['CorpusId:470667', '10.2139/ssrn.2250500', '0f40b1f08821e22e859c6050916cec3667778613']}
    DEBUG:semanticscholar:cURL command: curl -X POST -H 'x-api-key: F@k3K3y' -d '{"ids": ["CorpusId:470667", "10.2139/ssrn.2250500", "0f40b1f08821e22e859c6050916cec3667778613"]}' https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,year

.. warning::

    Be cautious when enabling debug logging and sharing the output, as it may contain sensitive information like API keys.

Debugging with the ``curl`` command
-----------------------------------

The ``semanticscholar`` library provides a ``curl`` command in its debug output. You can use this command to interact directly with the Semantic Scholar API and compare the results with those obtained through the library.

For example::

   curl -X POST -H 'x-api-key: F@k3K3y' -d '{"ids": ["CorpusId:470667", "10.2139/ssrn.2250500", "0f40b1f08821e22e859c6050916cec3667778613"]}' https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,year

You can also use any HTTP client of your choice (e.g., Postman) to replicate the request and validate the behavior.

By using debug logging and the provided ``curl`` command, you can isolate issues, verify API responses, and resolve problems effectively.
