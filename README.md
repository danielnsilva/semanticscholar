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
Can be used to access both the public API or the S2 Data Partner's API using a private key.

## Paper Lookup (Public API)
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
'Alan M. Turing'
2262347
```

## Author Lookup (Public API)
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

## Optional arguments
For each request, you can specify the timeout length, and whether or not to retrieve references unknown to Semantic Scholar. The default behaviour is `timeout=2` and `include_unknown_references=False`.
Alternatively, you can change these defaults for requests by providing the additional arguments when instantiating the `SemanticScholar` class:
```python
>>> from semanticscholar import SemanticScholar
>>> sch = SemanticScholar(timeout=5, include_unknown_references=True)
>>> paper = sch.paper('0796f6cd7f0403a854d67d525e9b32af3b277331')
>>> for ref in paper['references']:
...     if not ref['paperId']: print(ref['title'])
...
'Corpusbased method for automatic identification of support'
'Automatically constructing extraction patterns from untagged text'
'Corpusbased method for automatic identification of support verbs for nominalizations'
'Stretched Verb Constructions in English Routledge Studies in Germanic Linguistics. Routledge (Taylor and Francis)'
', Aria Haghighi , and Christopher D . Manning . 2008 . A global joint model for semantic role labeling'
'On-demand information extraction Association for Computational Lin- guistics'
```

## Accessing the Data Partner's API
Lastly, if you are a Semantic Scholar Data Partner, you can provide the URL and private key as optional arguments:
```python
>>> from semanticscholar import SemanticScholar
>>> s2_api_url = 'https://partner.semanticscholar.org/v1'
>>> s2_api_key = '40-CharacterPrivateKeyProvidedToPartners'
>>> sch = SemanticScholar(api_url=s2_api_url, api_key=s2_api_key)
```
