from semanticscholar.Paper import Paper
from semanticscholar.BaseReference import BaseReference


class Reference(BaseReference):
    '''
    This class abstracts a reference.
    '''

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        if 'citedPaper' in data:
            self._paper = Paper(data['citedPaper'])
