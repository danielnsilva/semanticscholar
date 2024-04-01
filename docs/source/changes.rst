:tocdepth: 2

Changelog
=========

All notable changes to this project will be documented in this file.

The format is based on `Keep a
Changelog <https://keepachangelog.com/en/1.1.0/>`__, and this project
adheres to `Semantic
Versioning <https://semver.org/spec/v2.0.0.html>`__.

`Unreleased <https://github.com/danielnsilva/semanticscholar/compare/v0.8.0...HEAD>`__
--------------------------------------------------------------------------------------

`0.8.0 <https://github.com/danielnsilva/semanticscholar/compare/v0.7.0...v0.8.0>`__ - 2024-03-15
------------------------------------------------------------------------------------------------

New Features
~~~~~~~~~~~~

-  Added support for returning a list of not found paper IDs in
   ``get_papers()``.
   (`3eb5516 <https://github.com/danielnsilva/semanticscholar/commit/3eb5516>`__)
-  Added support for bulk retrieval in ``search_paper()``.
   (`0fa8aac <https://github.com/danielnsilva/semanticscholar/commit/0fa8aac>`__)
-  Added support for disabling retrying when getting HTTP status 429 by
   `@qiankunli <https://github.com/qiankunli>`__ in
   `#84 <https://github.com/danielnsilva/semanticscholar/pull/84>`__

Bug Fixes
~~~~~~~~~

-  Fixed
   `#80 <https://github.com/danielnsilva/semanticscholar/issues/80>`__:
   ``get_papers()`` fails when one of the IDs was not found.
   (`3eb5516 <https://github.com/danielnsilva/semanticscholar/commit/3eb5516>`__)

.. _section-1:

`0.7.0 <https://github.com/danielnsilva/semanticscholar/compare/v0.6.0...v0.7.0>`__ - 2023-12-29
------------------------------------------------------------------------------------------------

.. _new-features-1:

New Features
~~~~~~~~~~~~

-  Debug mode
   (`fb249e9 <https://github.com/danielnsilva/semanticscholar/commit/fb249e9>`__)
-  Added new query parameters to search_paper():

   -  publication_date_or_year
      (`ed4cf6f <https://github.com/danielnsilva/semanticscholar/commit/ed4cf6f>`__)
   -  min_citation_count
      (`ab1cc67 <https://github.com/danielnsilva/semanticscholar/commit/ab1cc67>`__)

-  Added contextsWithIntent property for Citation and Reference
   (`c278e5d <https://github.com/danielnsilva/semanticscholar/commit/c278e5d>`__)
-  Added citationStyles property to Paper
   (`1e7e6b0 <https://github.com/danielnsilva/semanticscholar/commit/1e7e6b0>`__)

Enhancements
~~~~~~~~~~~~

-  Increased the default timeout value from 10 to 30 seconds
   (`e5aa367 <https://github.com/danielnsilva/semanticscholar/commit/e5aa367>`__)
-  Reduced the limit parameter (from 1000 to 100) to avoid timeout error
   and improve performance
   (`846e824 <https://github.com/danielnsilva/semanticscholar/commit/846e824>`__)

Breaking Changes
~~~~~~~~~~~~~~~~

-  Removed deprecated aliases property from Author
   (`202945c <https://github.com/danielnsilva/semanticscholar/commit/202945c>`__)

.. _section-2:

`0.6.0 <https://github.com/danielnsilva/semanticscholar/compare/v0.5.0...v0.6.0>`__ - 2023-11-26
------------------------------------------------------------------------------------------------

.. _new-features-2:

New Features
~~~~~~~~~~~~

-  Added support for asynchronous requests by
   `@gabriel-trigo <https://github.com/gabriel-trigo>`__ in
   `#56 <https://github.com/danielnsilva/semanticscholar/pull/56>`__
-  Added ``pool_from`` parameter in ``get_recommended_papers()``
   (d245515)

.. _bug-fixes-1:

Bug Fixes
~~~~~~~~~

-  Fixed the maximum sum of offset and limit from 10,000 to 1,000
   (908838a)

.. _breaking-changes-1:

Breaking Changes
~~~~~~~~~~~~~~~~

-  Removed deprecated URL ``partner.semanticscholar.org`` (01c9988)
-  Replaced `requests <https://requests.readthedocs.io/en/latest/>`__
   with `httpx <https://www.python-httpx.org/>`__ for asynchronous
   support

.. _section-3:

`0.5.0 <https://github.com/danielnsilva/semanticscholar/compare/v0.4.1...v0.5.0>`__ - 2023-08-11
------------------------------------------------------------------------------------------------

.. _new-features-3:

New Features
~~~~~~~~~~~~

-  Added support for Recommendations API.
   (`ef26088 <https://github.com/danielnsilva/semanticscholar/commit/ef26088>`__)

.. _breaking-changes-2:

Breaking Changes
~~~~~~~~~~~~~~~~

-  Spelling fixes object not found exception by
   `@shauryr <https://github.com/shauryr>`__ in
   `#54 <https://github.com/danielnsilva/semanticscholar/pull/54>`__
-  Removed deprecated parameter ``graph_api``.
   (`4fe2245 <https://github.com/danielnsilva/semanticscholar/commit/4fe2245>`__)
-  Removed deprecated parameter ``include_unknown_refs``.
   (`4f188c8 <https://github.com/danielnsilva/semanticscholar/commit/4f188c8>`__)

.. _section-4:

`0.4.1 <https://github.com/danielnsilva/semanticscholar/compare/v0.4.0...v0.4.1>`__ - 2023-04-01
------------------------------------------------------------------------------------------------

.. _new-features-4:

New Features
~~~~~~~~~~~~

-  Added new query parameters to ``search_paper()``:
   ``publicationTypes``, ``openAccessPdf``, and ``venue``.
   (`79a86ed <https://github.com/danielnsilva/semanticscholar/commit/79a86ed>`__)

.. _bug-fixes-2:

Bug Fixes
~~~~~~~~~

-  Fixed fields of study query parameter name.
   (`2e3b97a <https://github.com/danielnsilva/semanticscholar/commit/2e3b97a>`__)

.. _section-5:

`0.4.0 <https://github.com/danielnsilva/semanticscholar/compare/v0.3.2...v0.4.0>`__ - 2023-01-23
------------------------------------------------------------------------------------------------

.. _new-features-5:

New Features
~~~~~~~~~~~~

-  Added support for getting multiple papers or authors at once.
   (`eba2372 <https://github.com/danielnsilva/semanticscholar/commit/eba2372>`__)
-  Added support for getting details about paper’s author, citation and
   references.
   (`bd9e19a <https://github.com/danielnsilva/semanticscholar/commit/bd9e19a>`__,
   `0397761 <https://github.com/danielnsilva/semanticscholar/commit/0397761>`__,
   `6b4f2c7 <https://github.com/danielnsilva/semanticscholar/commit/6b4f2c7>`__)
-  Added support for getting details about author’s papers.
   (`f186cea <https://github.com/danielnsilva/semanticscholar/commit/f186cea>`__)
-  ``get_author()`` and ``get_paper()`` should now raise an
   ``ObjectNotFoundExeception`` when the Paper or Author ID is not
   found.
   (`ae50750 <https://github.com/danielnsilva/semanticscholar/commit/ae50750>`__)
-  New ``Paper`` properties: ``corpusId``, ``openAccessPdf``, and
   ``publicationVenue``.
   (`b2ae2bb <https://github.com/danielnsilva/semanticscholar/commit/b2ae2bb>`__)
-  New type: ``PublicationVenue``.
   (`648bd77 <https://github.com/danielnsilva/semanticscholar/commit/648bd77>`__)
-  Added support for 500 and 504 HTTP errors.
   (`c53c08c <https://github.com/danielnsilva/semanticscholar/commit/c53c08c>`__,
   `ec23182 <https://github.com/danielnsilva/semanticscholar/commit/ec23182>`__)

.. _enhancements-1:

Enhancements
~~~~~~~~~~~~

-  The ``ValueError`` exception will be raised when the ``limit``
   parameter is given a value that is out of bounds.

.. _breaking-changes-3:

Breaking Changes
~~~~~~~~~~~~~~~~

-  ``ObjectNotFoundExeception`` raised instead of returning an empty
   ``dict``.
-  Removed deprecated methods: ``author()`` and ``paper()``.
   (`06a6a53 <https://github.com/danielnsilva/semanticscholar/commit/06a6a53>`__)

Deprecations
~~~~~~~~~~~~

-  Deprecated ``graph_api`` parameter.
   (`4acbd11 <https://github.com/danielnsilva/semanticscholar/commit/4acbd11>`__)
-  Deprecated ``include_unknown_refs`` parameter in ``get_paper()``.
   (`1d74d22 <https://github.com/danielnsilva/semanticscholar/commit/1d74d22>`__)

.. _section-6:

`0.3.2 <https://github.com/danielnsilva/semanticscholar/compare/v0.3.1...v0.3.2>`__ - 2022-12-25
------------------------------------------------------------------------------------------------

.. _bug-fixes-3:

Bug Fixes
~~~~~~~~~

-  Fixed duplicated items issue on traversing results
   (`211bc5d <https://github.com/danielnsilva/semanticscholar/commit/211bc5d>`__)

.. _section-7:

`0.3.1 <https://github.com/danielnsilva/semanticscholar/compare/v0.3.0...v0.3.1>`__ - 2022-11-25
------------------------------------------------------------------------------------------------

.. _bug-fixes-4:

Bug Fixes
~~~~~~~~~

-  Fixed
   `#43 <https://github.com/danielnsilva/semanticscholar/issues/43>`__:
   default Partner’s API URL
   (`692d1c7 <https://github.com/danielnsilva/semanticscholar/commit/692d1c7>`__)

.. _section-8:

`0.3.0 <https://github.com/danielnsilva/semanticscholar/compare/v0.2.1...v0.3.0>`__ - 2022-09-18
------------------------------------------------------------------------------------------------

.. _new-features-6:

New Features
~~~~~~~~~~~~

-  Added support to the new Academic Graph API and its endpoints,
   including paper and author search.
-  Library rewrite using the abstraction design instead of a simple API
   wrapping. Response fields are accessible as properties, but key-based
   access is still available.

.. _enhancements-2:

Enhancements
~~~~~~~~~~~~

-  Increased the default timeout of API responses to 10 seconds.
   (`416b271 <https://github.com/danielnsilva/semanticscholar/commit/416b271>`__)

.. _breaking-changes-4:

Breaking Changes
~~~~~~~~~~~~~~~~

-  Removed direct access to deprecated methods ``paper()`` and
   ``author()``.
   (`42d28ca <https://github.com/danielnsilva/semanticscholar/commit/42d28ca>`__)

.. _deprecations-1:

Deprecations
~~~~~~~~~~~~

-  Deprecated ``paper()`` and ``author()`` methods in
   ``SemanticScholar`` class, which are substituted by ``get_paper()``
   and ``get_author()``.
   (`75d299b <https://github.com/danielnsilva/semanticscholar/commit/75d299b>`__)

.. _section-9:

`0.2.1 <https://github.com/danielnsilva/semanticscholar/compare/v0.2.0...v0.2.1>`__ - 2021-11-02
------------------------------------------------------------------------------------------------

.. _bug-fixes-5:

Bug Fixes
~~~~~~~~~

-  Fixed API URL definition issue
   (`eee1df9 <https://github.com/danielnsilva/semanticscholar/commit/eee1df9>`__)

.. _section-10:

`0.2.0 <https://github.com/danielnsilva/semanticscholar/compare/v0.1.6...v0.2.0>`__ - 2021-10-31
------------------------------------------------------------------------------------------------

.. _new-features-7:

New Features
~~~~~~~~~~~~

-  Added support for S2 Data Partner’s API by
   `@nilsjor <https://github.com/nilsjor>`__ in
   `#15 <https://github.com/danielnsilva/semanticscholar/pull/15>`__

.. _section-11:

`0.1.6 <https://github.com/danielnsilva/semanticscholar/compare/v0.1.5...v0.1.6>`__ - 2021-09-11
------------------------------------------------------------------------------------------------

.. _new-features-8:

New Features
~~~~~~~~~~~~

-  Added timeout to semanticscholar requests by
   `@wyh <https://github.com/wyh>`__ in
   `#7 <https://github.com/danielnsilva/semanticscholar/pull/7>`__

.. _section-12:

`0.1.5 <https://github.com/danielnsilva/semanticscholar/compare/v0.1.4...v0.1.5>`__ - 2020-08-18
------------------------------------------------------------------------------------------------

.. _enhancements-3:

Enhancements
~~~~~~~~~~~~

-  Fixed API http type by `@wyh <https://github.com/wyh>`__ in
   `#6 <https://github.com/danielnsilva/semanticscholar/pull/6>`__

.. _section-13:

`0.1.4 <https://github.com/danielnsilva/semanticscholar/compare/v0.1.3...v0.1.4>`__ - 2020-03-04
------------------------------------------------------------------------------------------------

Dependencies
~~~~~~~~~~~~

-  New retrying library `tenacity <http://tenacity.readthedocs.io/>`__
   (`69e53c9 <https://github.com/danielnsilva/semanticscholar/commit/69e53c998f538e7f4c9a1ffff8eba6873deae3b4>`__)

.. _section-14:

`0.1.3 <https://github.com/danielnsilva/semanticscholar/releases/tag/v0.1.3>`__ - 2019-08-02
--------------------------------------------------------------------------------------------
