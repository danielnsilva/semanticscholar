class SemanticScholarException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BadQueryParametersException(SemanticScholarException):
    pass
