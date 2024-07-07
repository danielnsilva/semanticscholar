class SemanticScholarException(Exception):
    '''A base class for exceptions.'''

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BadQueryParametersException(SemanticScholarException):
    '''Invalid query params or unsupported fields.'''


class ObjectNotFoundException(SemanticScholarException):
    '''Paper or Author ID not found.'''

class NoMorePagesException(SemanticScholarException):
    '''No more pages to fetch.'''

class ServerErrorException(SemanticScholarException):
    '''A base class for HTTP Status Code 5xx errors.'''

class InternalServerErrorException(ServerErrorException):
    '''HTTP Status Code 500.'''

class GatewayTimeoutException(ServerErrorException):
    '''HTTP Status Code 504.'''
