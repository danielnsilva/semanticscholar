# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.9.0] - 2024-11-30

### New Features

- Added support for paper title search. ([3a3f797](https://github.com/danielnsilva/semanticscholar/commit/3a3f797))

### Enhancements

- Added asynchronous iterator for `PaginatedResults` by [@rgeronimi](https://github.com/rgeronimi) in [#95](https://github.com/danielnsilva/semanticscholar/pull/95)

### Bug Fixes

- Removed unnecessary `nest_asyncio.apply()` call when using the library in asynchronous mode by [@rgeronimi](https://github.com/rgeronimi) in [#95](https://github.com/danielnsilva/semanticscholar/pull/95)

## [0.8.4] - 2024-07-08

### Enhancements

- Replaced debug parameter with Python's standard logging in DEBUG level. ([d5bfa38](https://github.com/danielnsilva/semanticscholar/commit/d5bfa38))
- Added specific exceptions for requests responses: `InternalServerErrorException` (HTTP Status 500), `GatewayTimeoutException` (HTTP Status 504), and `ServerErrorException` (base class for HTTP Status 5xx). ([298997f](https://github.com/danielnsilva/semanticscholar/commit/298997f))

### Deprecations

- Deprecated `debug` parameter. ([d5bfa38](https://github.com/danielnsilva/semanticscholar/commit/d5bfa38))

## [0.8.3]

- Version `0.8.3` was not released due to issues in the release process.

## [0.8.2] - 2024-05-31

### Bug Fixes

- Removed deprecated `authors.aliases` from `Paper`. ([ed92c37](https://github.com/danielnsilva/semanticscholar/commit/ed92c37))
- Fixed error generating cURL command. ([bc5c916](https://github.com/danielnsilva/semanticscholar/commit/bc5c916))

## [0.8.1] - 2024-05-17

### Bug Fixes

- Fixed [#87](https://github.com/danielnsilva/semanticscholar/issues/87): `get_authors()` fails when one of the IDs was not found. ([ae03dbb](https://github.com/danielnsilva/semanticscholar/commit/ae03dbb))

## [0.8.0] - 2024-03-15

### New Features

- Added support for returning a list of not found paper IDs in `get_papers()`. ([3eb5516](https://github.com/danielnsilva/semanticscholar/commit/3eb5516))
- Added support for bulk retrieval in `search_paper()`. ([0fa8aac](https://github.com/danielnsilva/semanticscholar/commit/0fa8aac))
- Added support for disabling retrying when getting HTTP status 429 by [@qiankunli](https://github.com/qiankunli) in [#84](https://github.com/danielnsilva/semanticscholar/pull/84)

### Bug Fixes

- Fixed [#80](https://github.com/danielnsilva/semanticscholar/issues/80): `get_papers()` fails when one of the IDs was not found. ([3eb5516](https://github.com/danielnsilva/semanticscholar/commit/3eb5516))

## [0.7.0] - 2023-12-29

### New Features

- Debug mode ([fb249e9](https://github.com/danielnsilva/semanticscholar/commit/fb249e9))
- Added new query parameters to search_paper():
    - publication_date_or_year ([ed4cf6f](https://github.com/danielnsilva/semanticscholar/commit/ed4cf6f))
    - min_citation_count ([ab1cc67](https://github.com/danielnsilva/semanticscholar/commit/ab1cc67))
- Added contextsWithIntent property for Citation and Reference ([c278e5d](https://github.com/danielnsilva/semanticscholar/commit/c278e5d))
- Added citationStyles property to Paper ([1e7e6b0](https://github.com/danielnsilva/semanticscholar/commit/1e7e6b0))

### Enhancements

- Increased the default timeout value from 10 to 30 seconds ([e5aa367](https://github.com/danielnsilva/semanticscholar/commit/e5aa367))
- Reduced the limit parameter (from 1000 to 100) to avoid timeout error and improve performance ([846e824](https://github.com/danielnsilva/semanticscholar/commit/846e824))

### Breaking Changes

- Removed deprecated aliases property from Author ([202945c](https://github.com/danielnsilva/semanticscholar/commit/202945c))

## [0.6.0] - 2023-11-26

### New Features

- Added support for asynchronous requests by [@gabriel-trigo](https://github.com/gabriel-trigo) in [#56](https://github.com/danielnsilva/semanticscholar/pull/56)
- Added `pool_from` parameter in `get_recommended_papers()` (d245515)

### Bug Fixes

- Fixed the maximum sum of offset and limit from 10,000 to 1,000 (908838a)

### Breaking Changes

- Removed deprecated URL `partner.semanticscholar.org` (01c9988)
- Replaced [requests](https://requests.readthedocs.io/en/latest/) with [httpx](https://www.python-httpx.org/) for asynchronous support

## [0.5.0] - 2023-08-11

### New Features

- Added support for Recommendations API. ([ef26088](https://github.com/danielnsilva/semanticscholar/commit/ef26088))

### Breaking Changes

- Spelling fixes object not found exception by [@shauryr](https://github.com/shauryr) in [#54](https://github.com/danielnsilva/semanticscholar/pull/54)
- Removed deprecated parameter `graph_api`. ([4fe2245](https://github.com/danielnsilva/semanticscholar/commit/4fe2245))
- Removed deprecated parameter `include_unknown_refs`. ([4f188c8](https://github.com/danielnsilva/semanticscholar/commit/4f188c8))

## [0.4.1] - 2023-04-01

### New Features

- Added new query parameters to `search_paper()`: `publicationTypes`, `openAccessPdf`, and `venue`. ([79a86ed](https://github.com/danielnsilva/semanticscholar/commit/79a86ed))

### Bug Fixes

- Fixed fields of study query parameter name. ([2e3b97a](https://github.com/danielnsilva/semanticscholar/commit/2e3b97a))

## [0.4.0] - 2023-01-23

### New Features

- Added support for getting multiple papers or authors at once. ([eba2372](https://github.com/danielnsilva/semanticscholar/commit/eba2372))
- Added support for getting details about paper's author, citation and references. ([bd9e19a](https://github.com/danielnsilva/semanticscholar/commit/bd9e19a), [0397761](https://github.com/danielnsilva/semanticscholar/commit/0397761), [6b4f2c7](https://github.com/danielnsilva/semanticscholar/commit/6b4f2c7))
- Added support for getting details about author's papers. ([f186cea](https://github.com/danielnsilva/semanticscholar/commit/f186cea))
- `get_author()` and `get_paper()` should now raise an `ObjectNotFoundExeception` when the Paper or Author ID is not found. ([ae50750](https://github.com/danielnsilva/semanticscholar/commit/ae50750))
- New `Paper` properties: `corpusId`, `openAccessPdf`, and `publicationVenue`. ([b2ae2bb](https://github.com/danielnsilva/semanticscholar/commit/b2ae2bb))
- New type: `PublicationVenue`. ([648bd77](https://github.com/danielnsilva/semanticscholar/commit/648bd77))
- Added support for 500 and 504 HTTP errors. ([c53c08c](https://github.com/danielnsilva/semanticscholar/commit/c53c08c), [ec23182](https://github.com/danielnsilva/semanticscholar/commit/ec23182))

### Enhancements

- The `ValueError` exception will be raised when the `limit` parameter is given a value that is out of bounds.

### Breaking Changes

- `ObjectNotFoundExeception` raised instead of returning an empty `dict`.
- Removed deprecated methods: `author()` and `paper()`. ([06a6a53](https://github.com/danielnsilva/semanticscholar/commit/06a6a53))

### Deprecations

- Deprecated `graph_api` parameter. ([4acbd11](https://github.com/danielnsilva/semanticscholar/commit/4acbd11))
- Deprecated `include_unknown_refs` parameter in `get_paper()`. ([1d74d22](https://github.com/danielnsilva/semanticscholar/commit/1d74d22))

## [0.3.2] - 2022-12-25

### Bug Fixes
- Fixed duplicated items issue on traversing results ([211bc5d](https://github.com/danielnsilva/semanticscholar/commit/211bc5d))

## [0.3.1] - 2022-11-25

### Bug Fixes
- Fixed [#43](https://github.com/danielnsilva/semanticscholar/issues/43): default Partner's API URL ([692d1c7](https://github.com/danielnsilva/semanticscholar/commit/692d1c7))

## [0.3.0] - 2022-09-18

### New Features

- Added support to the new Academic Graph API and its endpoints, including paper and author search.
- Library rewrite using the abstraction design instead of a simple API wrapping. Response fields are accessible as properties, but key-based access is still available.

### Enhancements

- Increased the default timeout of API responses to 10 seconds. ([416b271](https://github.com/danielnsilva/semanticscholar/commit/416b271))

### Breaking Changes

- Removed direct access to deprecated methods `paper()` and `author()`. ([42d28ca](https://github.com/danielnsilva/semanticscholar/commit/42d28ca))

### Deprecations

- Deprecated `paper()` and `author()` methods in `SemanticScholar` class, which are substituted by `get_paper()` and `get_author()`. ([75d299b](https://github.com/danielnsilva/semanticscholar/commit/75d299b))

## [0.2.1] - 2021-11-02

### Bug Fixes

- Fixed API URL definition issue ([eee1df9](https://github.com/danielnsilva/semanticscholar/commit/eee1df9))

## [0.2.0] - 2021-10-31

### New Features

- Added support for S2 Data Partner's API by [@nilsjor](https://github.com/nilsjor) in [#15](https://github.com/danielnsilva/semanticscholar/pull/15)

## [0.1.6] - 2021-09-11

### New Features

- Added timeout to semanticscholar requests by [@wyh](https://github.com/wyh) in [#7](https://github.com/danielnsilva/semanticscholar/pull/7)

## [0.1.5] - 2020-08-18

### Enhancements

- Fixed API http type by [@wyh](https://github.com/wyh) in [#6](https://github.com/danielnsilva/semanticscholar/pull/6)

## [0.1.4] - 2020-03-04

### Dependencies

- New retrying library [tenacity](http://tenacity.readthedocs.io/) ([69e53c9](https://github.com/danielnsilva/semanticscholar/commit/69e53c998f538e7f4c9a1ffff8eba6873deae3b4))

## [0.1.3] - 2019-08-02

[unreleased]: https://github.com/danielnsilva/semanticscholar/compare/v0.9.0...HEAD
[0.9.0]: https://github.com/danielnsilva/semanticscholar/compare/v0.8.4...v0.9.0
[0.8.4]: https://github.com/danielnsilva/semanticscholar/compare/v0.8.2...v0.8.4
[0.8.2]: https://github.com/danielnsilva/semanticscholar/compare/v0.8.1...v0.8.2
[0.8.1]: https://github.com/danielnsilva/semanticscholar/compare/v0.8.0...v0.8.1
[0.8.0]: https://github.com/danielnsilva/semanticscholar/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/danielnsilva/semanticscholar/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/danielnsilva/semanticscholar/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/danielnsilva/semanticscholar/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/danielnsilva/semanticscholar/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/danielnsilva/semanticscholar/compare/v0.3.2...v0.4.0
[0.3.2]: https://github.com/danielnsilva/semanticscholar/compare/v0.3.1...v0.3.2
[0.3.1]: https://github.com/danielnsilva/semanticscholar/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/danielnsilva/semanticscholar/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/danielnsilva/semanticscholar/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/danielnsilva/semanticscholar/compare/v0.1.6...v0.2.0
[0.1.6]: https://github.com/danielnsilva/semanticscholar/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/danielnsilva/semanticscholar/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/danielnsilva/semanticscholar/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/danielnsilva/semanticscholar/releases/tag/v0.1.3
