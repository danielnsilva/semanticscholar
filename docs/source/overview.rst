===============
semanticscholar
===============

Unofficial Python client library for `Semantic Scholar APIs <https://api.semanticscholar.org/>`_.

Main features
=============

- Simplified access to the Semantic Scholar APIs
- Support for the Academic Graph and Recommendations APIs
- Typed responses
- Rate limiting management (with retries)
- Support for asynchronous requests

Quickstart
==========

Installation
------------

.. code-block:: bash

    pip install semanticscholar

See the :doc:`install` page for more detailed installation instructions.

Usage
-----

.. code-block:: python

   # First, import the client from semanticscholar module
   from semanticscholar import SemanticScholar

   # You'll need an instance of the client to request data from the API
   sch = SemanticScholar()

   # Get a paper by its ID
   paper = sch.get_paper('10.1093/mind/lix.236.433')

   # Print the paper title
   print(paper.title)

Output:

.. code-block:: text

   Computing Machinery and Intelligence

What next?
----------

- :doc:`usage` - See additional examples to learn how to use the library to fetch data from Semantic Scholar APIs.
- :doc:`reference` - Get the details of the classes and methods available in the library.
- :doc:`api` - Check the supported SemanticScholar API endpoints and which methods implement them.

Semantic Scholar API official docs and additional resources
===========================================================

If you have concerns or feedback specific to this library, feel free to `open an issue <https://github.com/danielnsilva/semanticscholar/issues>`_. However, the official documentation provides additional resources for broader API-related issues.

- For details on Semantic Scholar APIs capabilities and limits, `go to the official documentation <https://api.semanticscholar.org/api-docs/graph>`_.
- The `Frequently Asked Questions <https://www.semanticscholar.org/faq>`_ page also provides helpful content if you need a better understanding of data fetched from Semantic Scholar services.
- This `official GitHub repository <https://github.com/allenai/s2-folks>`_ allows users to report issues and suggest improvements.

Contributing
============

As a volunteer-maintained open-source project, contributions of all forms are welcome! For more information, see the :doc:`contributing`.

Please make sure to understand our :doc:`code_of_conduct` before you contribute. TL;DR: Be nice and respectful!

License
=======

This project is licensed under the MIT License - see the :doc:`license` file for details.
