class SemanticScholarException(Exception):
    '''A base class for exceptions.'''

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BadQueryParametersException(SemanticScholarException):
    '''Invalid query params or unsupported fields.'''


class ObjectNotFoundException(SemanticScholarException):
    '''Paper or Author ID not found'''
