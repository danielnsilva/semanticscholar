# semanticscholar

[![Latest version](https://img.shields.io/pypi/v/semanticscholar?style=for-the-badge)](https://pypi.org/project/semanticscholar)
![PyPI - Downloads](https://img.shields.io/pypi/dm/semanticscholar?style=for-the-badge)
[![GitHub license](https://img.shields.io/github/license/danielnsilva/semanticscholar?style=for-the-badge)](https://github.com/danielnsilva/semanticscholar/blob/master/LICENSE)
[![Codacy grade](https://img.shields.io/codacy/grade/1456603c25764b14b441ed509e938154?style=for-the-badge)](https://www.codacy.com/gh/danielnsilva/semanticscholar/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=danielnsilva/semanticscholar&amp;utm_campaign=Badge_Grade)

Unofficial [Semantic Scholar Academic Graph API](https://api.semanticscholar.org/) client library for Python.

![](search_paper.gif)

## How to install
```console
pip install semanticscholar
```

## Usage
Programmatically retrieve paper and author data by ID or query string.
Can be used to access both the public API and the S2 Data Partner's API using a private key.

### Paper Lookup
To access paper data:
```python
from semanticscholar import SemanticScholar
sch = SemanticScholar()
paper = sch.get_paper('10.1093/mind/lix.236.433')
paper.title
```

Output:
```console
'Computing Machinery and Intelligence'
```

### Author Lookup
To access author data:
```python
from semanticscholar import SemanticScholar
sch = SemanticScholar()
author = sch.get_author(2262347)
author.name
```

Output:
```console
'Alan M. Turing'
```

### Search for papers and authors
To search for papers by keyword:
```python
from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_paper('Computing Machinery and Intelligence')
print(f'{results.total} results.', f'First occurrence: {results[0].title}.')
```

Output:
```console
492 results. First occurrence: Computing Machinery and Intelligence.
```
To search for authors by keyword:
```python
from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_author('Alan M. Turing')
print(f'{results.total} results.', f'First occurrence: {results[0].title}.')
```

Output:
```console
4 results. First occurrence: A. Turing.
```

### Traversing search results

Each call to ```search_paper()``` and ```search_author()``` will paginate through results, returning the list of papers or authors up to the bound limit (default value is 100). You can retrieve the next batch of results by calling ```next_page()``` or simply iterating over all of them:

```python
from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_paper('Computing Machinery and Intelligence')
for item in results:
     print(item.title)
```

Output:
```console
Computing Machinery and Intelligence
Computing Machinery and Intelligence (1950)
Artificial intelligence in the research of consciousness and in social life (in honor of 70-years anniversary of A. Turing’s paper “Computing Machinery and Intelligence” (papers of the “round table”)
Studies on computing machinery and intelligence
On Computing Machinery and Intelligence
...
Information revolution: Impact of technology on global workforce
```

When iterating over the return of search methods, the client library will always traverse all results regardless of the number of pages. If just the first batch is enough, you can avoid more calls to API, handling only current results:

```python
from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_paper('Computing Machinery and Intelligence')
for item in results.items:
     print(item.title)
```

Output:
```console
Computing Machinery and Intelligence
Computing Machinery and Intelligence (1950)
Artificial intelligence in the research of consciousness and in social life (in honor of 70-years anniversary of A. Turing’s paper “Computing Machinery and Intelligence” (papers of the “round table”)
Studies on computing machinery and intelligence
On Computing Machinery and Intelligence
...
Building Thinking Machines by Solving Animal Cognition Tasks
```

### Query parameters for all methods

#### ```fields: list```

The list of the fields to be returned. By default, the response includes all fields. As explained in [official documentation](https://api.semanticscholar.org/api-docs/graph) , fields like papers (author lookup and search) may result responses bigger than the usual size and affect performance. Consider reducing the list. Check [official documentation](https://api.semanticscholar.org/api-docs/graph) for a list of available fields.

### Query parameters for all search methods

#### ```limit: int```

This parameter represents the maximum number of results to return on each call to API, and its value can't be higher than 100, which is the default value. According to [official documentation](https://api.semanticscholar.org/api-docs/graph), setting a smaller limit reduces output size and latency.

```python
from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_paper('software engineering', limit=5)
len(results)
```

Output:
```console
5
```

### Query parameters for search papers

#### ```year: str```

Restrict results to a specific publication year or a given range, following the patterns '{year}' or '{start}-{end}'. Also you can omit the start or the end. Examples: '2000', '1991-2000', '1991-', '-2000'.

```python
from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_paper('software engineering', year=2000)
results[0].year
```

Output:
```console
2000
```

#### ```fields_of_study: list```

Restrict results to a given list of fields of study. Check [official documentation](https://api.semanticscholar.org/api-docs/graph#tag/Paper-Data/operation/get_graph_get_paper_search) for a list of available fields.

```python
from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_paper('software engineering', fields_of_study=['Computer Science','Education'])
results[0].s2FieldsOfStudy
```

Output:
```console
[{'category': 'Computer Science', 'source': 'external'}, {'category': 'Computer Science', 'source': 's2-fos-model'}]
```

### Other options

#### ```timeout: int```

You can set the wait time for a response. By default, requests to API will wait for 10 seconds until the Timeout Exception raises. To change the default value, specify it at instance creation of ```SemanticScholar``` class:

```python
from semanticscholar import SemanticScholar
sch = SemanticScholar(timeout=5)
```

or set ```timeout``` property value:

```python
from semanticscholar import SemanticScholar
sch = SemanticScholar()
sch.timeout = 5
```

### Accessing the Data Partner's API
If you are a Semantic Scholar Data Partner you can provide the private key as an optional argument:
```python
from semanticscholar import SemanticScholar
s2_api_key = '40-CharacterPrivateKeyProvidedToPartners'
sch = SemanticScholar(api_key=s2_api_key)
```

## Semantic Scholar Academic Graph API docs

To get more detailed information about Semantic Scholar Academic Graph API functionalities and limitations, [go to the official documentation](https://api.semanticscholar.org/api-docs/graph).
