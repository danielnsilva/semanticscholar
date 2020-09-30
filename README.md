# semanticscholar

[![Latest version](https://img.shields.io/pypi/v/semanticscholar)](https://pypi.org/project/semanticscholar)
[![GitHub license](https://img.shields.io/github/license/danielnsilva/semanticscholar)](https://github.com/danielnsilva/semanticscholar/blob/master/LICENSE)

A python library that aims to retrieve data from [Semantic Scholar API](https://api.semanticscholar.org/).

# How to install
```
pip install semanticscholar
```

# Usage
Programmatically access paper and author data.

## Paper Lookup
To access paper data:
```python
>>> from semanticscholar import SemanticScholar
>>> sch = SemanticScholar()
>>> paper = sch.paper('10.1093/mind/lix.236.433', timeout=2)
>>> paper.keys()
dict_keys(['abstract', 'arxivId', 'authors', 'citationVelocity', 'citations', 'doi',
'influentialCitationCount', 'paperId', 'references', 'title', 'topics', 'url', 'venue', 'year'])
>>> paper['title']
'Computing Machinery and Intelligence'
>>> for author in paper['authors']:
...     print(author['name'])
...     print(author['authorId'])
...
Alan M. Turing
2262347
```

## Author Lookup
To access author data:
```python
>>> from semanticscholar import SemanticScholar
>>> sch = SemanticScholar()
>>> author = sch.author(2262347, timeout=2)
>>> author.keys()
dict_keys(['aliases', 'authorId', 'citationVelocity', 'influentialCitationCount', 'name', 'papers', 'url'])
>>> author['name']
'Alan M. Turing'
>>> len(author['papers'])
77
```
