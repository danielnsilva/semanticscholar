from semanticscholar.SemanticScholarObject import SemanticScholarObject
from semanticscholar.Dataset import Dataset

class Release(SemanticScholarObject):
    '''
    This class represents a release version of the Semantic Scholar Datasets.
    '''

    FIELDS = [
        'release_id',
        'readme',
        'datasets'
    ]

    def __init__(self, data) -> None:
        '''
        Initialize Release object.

        :param dict data: Release data from the API.
        '''
        super().__init__()
        self._release_id = None
        self._readme = None
        self._datasets = None
        self._init_attributes(data)

    @property
    def release_id(self) -> str:
        '''
        Release identifier.

        :type: :class:`str`
        '''
        return self._release_id

    @property
    def readme(self) -> str:
        '''
        Release README.

        :type: :class:`str`
        '''
        return self._readme

    @property
    def datasets(self) -> list:
        '''
        List of datasets in this release.

        :type: :class:`list` of :class:`semanticscholar.Dataset.Dataset`
        '''
        return self._datasets

    def _init_attributes(self, data) -> None:
        self._data = data
        if 'release_id' in data:
            self._release_id = data['release_id']
        if 'README' in data:
            self._readme = data['README']
        if 'datasets' in data:
            self._datasets = [Dataset(dataset) for dataset in data['datasets']]
