from semanticscholar.SemanticScholarObject import SemanticScholarObject


class IncrementalUpdate(SemanticScholarObject):
    '''
    This class represents a single diff between two sequential releases of a dataset.
    '''

    FIELDS = [
        'from_release',
        'to_release',
        'update_files',
        'delete_files'
    ]

    def __init__(self, data) -> None:
        '''
        Initialize IncrementalUpdate object.

        :param dict data: Dataset diff data from the API.
        '''
        super().__init__()
        self._from_release = None
        self._to_release = None
        self._update_files = None
        self._delete_files = None
        self._init_attributes(data)

    @property
    def from_release(self) -> str:
        '''
        Baseline release for this diff.

        :type: :class:`str`
        '''
        return self._from_release

    @property
    def to_release(self) -> str:
        '''
        Target release for this diff.

        :type: :class:`str`
        '''
        return self._to_release

    @property
    def update_files(self) -> list:
        '''
        List of files that contain updates to the dataset.

        :type: :class:`list` of :class:`str`
        '''
        return self._update_files

    @property
    def delete_files(self) -> list:
        '''
        List of files that contain deletes from the dataset.

        :type: :class:`list` of :class:`str`
        '''
        return self._delete_files

    def _init_attributes(self, data) -> None:
        self._data = data
        if 'from_release' in data:
            self._from_release = data['from_release']
        if 'to_release' in data:
            self._to_release = data['to_release']
        if 'update_files' in data:
            self._update_files = data['update_files']
        if 'delete_files' in data:
            self._delete_files = data['delete_files']


class DatasetDiff(SemanticScholarObject):
    '''
    This class represents the complete diff information for a dataset between two releases,
    including the dataset name, release information, and list of individual diffs.
    '''

    FIELDS = [
        'dataset',
        'start_release',
        'end_release',
        'diffs'
    ]

    def __init__(self, data) -> None:
        '''
        Initialize DatasetDiff object.

        :param dict data: Dataset diffs data from the API.
        '''
        super().__init__()
        self._dataset = None
        self._start_release = None
        self._end_release = None
        self._diffs = None
        self._init_attributes(data)

    @property
    def dataset(self) -> str:
        '''
        Dataset name.

        :type: :class:`str`
        '''
        return self._dataset

    @property
    def start_release(self) -> str:
        '''
        Beginning release, i.e. the release currently held by the client.

        :type: :class:`str`
        '''
        return self._start_release

    @property
    def end_release(self) -> str:
        '''
        Ending release, i.e. the release the client wants to update to.

        :type: :class:`str`
        '''
        return self._end_release

    @property
    def diffs(self) -> list:
        '''
        List of diffs that need to be applied to bring the dataset at 'start_release' up to date with 'end_release'.

        :type: :class:`list` of :class:`semanticscholar.DatasetDiff.IncrementalUpdate`
        '''
        return self._diffs

    def _init_attributes(self, data) -> None:
        self._data = data
        if 'dataset' in data:
            self._dataset = data['dataset']
        if 'start_release' in data:
            self._start_release = data['start_release']
        if 'end_release' in data:
            self._end_release = data['end_release']
        if 'diffs' in data:
            self._diffs = [IncrementalUpdate(diff) for diff in data['diffs']]
