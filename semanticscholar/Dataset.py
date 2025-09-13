from semanticscholar.SemanticScholarObject import SemanticScholarObject


class Dataset(SemanticScholarObject):
    '''
    This class represents a particular dataset in a release version of the Semantic Scholar Datasets.
    '''

    FIELDS = [
        'name',
        'description',
        'readme',
        'files'
    ]

    def __init__(self, data) -> None:
        '''
        Initialize Dataset object.

        :param dict data: Dataset data from the API.
        '''
        super().__init__()
        self._name = None
        self._description = None
        self._readme = None
        self._files = None
        self._init_attributes(data)

    @property
    def name(self) -> str:
        '''
        Dataset name.

        :type: :class:`str`
        '''
        return self._name

    @property
    def description(self) -> str:
        '''
        Dataset description.

        :type: :class:`str`
        '''
        return self._description
    
    @property
    def readme(self) -> str:
        '''
        Dataset README.

        :type: :class:`str`
        '''
        return self._readme

    @property
    def files(self) -> list:
        '''
        List of file urls in the dataset.

        :type: :class:`list` of :class:`str`
        '''
        return self._files

    def _init_attributes(self, data) -> None:
        self._data = data
        if 'name' in data:
            self._name = data['name']
        if 'description' in data:
            self._description = data['description']
        if 'README' in data:
            self._readme = data['README']
        if 'files' in data:
            self._files = data['files']
