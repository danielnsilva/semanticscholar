from semanticscholar.Paper import Paper
from semanticscholar.BaseReference import BaseReference


class Citation(BaseReference):
    '''
    This class abstracts a citation.
    '''

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        if 'citingPaper' in data:
            self._paper = Paper(data['citingPaper'])
