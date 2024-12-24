Usage
-----

Basics
^^^^^^

Paginated results
~~~~~~~~~~~~~~~~~

Asynchronous requests
~~~~~~~~~~~~~~~~~~~~~

Authenticated requests
~~~~~~~~~~~~~~~~~~~~~~

Paper and Author
^^^^^^^^^^^^^^^^

Paper
~~~~~

To access paper data:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    paper = sch.get_paper('10.1093/mind/lix.236.433')
    print(paper.title)

Output:

.. code-block:: bash

    Computing Machinery and Intelligence

Author
~~~~~~

To access author data:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    author = sch.get_author(2262347)
    print(author.name)

Output:

.. code-block:: bash

    Alan M. Turing

Retrieve multiple items at once
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    for item in results:
        print(item.title)

Output:

.. code-block:: bash

    Improving Third-Party Audits and Regulatory Compliance in India
    How Much Should We Trust Differences-in-Differences Estimates?
    The Miracle of Microfinance? Evidence from a Randomized Evaluation

Get details for multiple authors:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    list_of_author_ids = ['3234559', '1726629', '1711844']
    results = sch.get_authors(list_of_author_ids)
    for item in results:
        print(item.name)

Output:

.. code-block:: bash

    E. Dijkstra
    D. Parnas
    I. Sommerville

Search by keyword
~~~~~~~~~~~~~~~~~

To search for papers by keyword:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.search_paper('Computing Machinery and Intelligence')
    print(f'{results.total} results.', f'First occurrence: {results[0].title}.')

Output:

.. code-block:: bash

    492 results. First occurrence: Computing Machinery and Intelligence.

.. warning::

    From the `official documentation <https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/get_graph_paper_relevance_search>`_: "Because of the subtleties of finding partial phrase matches in different parts of the document, be cautious about interpreting the total field as a count of documents containing any particular word in the query."

To search for authors by name:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.search_author('Alan M. Turing')
    print(f'{results.total} results.', f'First occurrence: {results[0].name}.')

Output:

.. code-block:: bash

    4 results. First occurrence: A. Turing.

Recommended papers
^^^^^^^^^^^^^^^^^^

To get recommended papers for a given paper:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    results = sch.get_recommended_papers('10.2139/ssrn.2250500')
    for item in results:
        print(item.title)

Output:

.. code-block:: bash

    Microcredit: Impacts and promising innovations
    MIT Open Access
    The Econmics of Badmouthing: Libel Law and the Underworld of the Financial Press in France before World War I
    Give Biden a 6-Point
    Getting more value from Australian Intergenerational Reports
    ...
    Structural Change and Economic Dynamics

To get recommended papers based on a list of positive and negative paper examples:

.. code-block:: python

    from semanticscholar import SemanticScholar
    sch = SemanticScholar()
    positive_paper_ids = ['10.1145/3544585.3544600']
    negative_paper_ids = ['10.1145/301250.301271']
    results = sch.get_recommended_papers_from_lists(positive_paper_ids, negative_paper_ids)
    for item in results:
        print(item.title)

Output:

.. code-block:: bash

    BUILDING MINIMUM SPANNING TREES BY LIMITED NUMBER OF NODES OVER TRIANGULATED SET OF INITIAL NODES
    Recognition of chordal graphs and cographs which are Cover-Incomparability graphs
    Minimizing Maximum Unmet Demand by Transportations Between Adjacent Nodes Characterized by Supplies and Demands
    Optimal Near-Linear Space Heaviest Induced Ancestors
    Diameter-2-critical graphs with at most 13 nodes
    ...
    Advanced Heuristic and Approximation Algorithms (M2)

You can also omit the list of negative paper IDs; in which case, the API will return recommended papers based on the list of positive paper IDs only.

Common query parameters
^^^^^^^^^^^^^^^^^^^^^^^

Troubleshooting
^^^^^^^^^^^^^^^
