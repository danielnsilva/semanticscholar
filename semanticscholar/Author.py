class Author:

    def __init__(self, data):
        self._init_attributes(data)

    @property
    def aliases(self):
        return self._aliases

    @property
    def authorId(self):
        return self._authorId

    @property
    def influentialCitationCount(self):
        return self._influentialCitationCount

    @property
    def name(self):
        return self._name

    @property
    def papers(self):
        return self._papers

    @property
    def url(self):
        return self._url

    @property
    def data(self):
        return self._data

    def _init_attributes(self, data):
        self._data = data
        if 'aliases' in data:
            self._aliases = data['aliases']
        if 'authorId' in data:
            self._authorId = data['authorId']
        if 'influentialCitationCount' in data:
            self._influentialCitationCount = data['influentialCitationCount']
        if 'name' in data:
            self._name = data['name']
        if 'papers' in data:
            self._papers = data['papers']
        if 'url' in data:
            self._url = data['url']
