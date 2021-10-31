from .SemanticScholar import SemanticScholar
import warnings


def paper(
            id: str,
            timeout: int=2,
            include_unknown_references: bool=False,
            api_key: str=None,
            api_url: str=None
        ) -> dict:
    '''Paper lookup

    :param str id: S2PaperId, DOI or ArXivId.
    :param float timeout: an exception is raised
        if the server has not issued a response for timeout seconds.
    :param bool include_unknown_references:
        (optional) include non referenced paper.
    :param str api_key: (optional) private API key.
    :param str api_url: (optional) custom API url.
    :returns: paper data or empty :class:`dict` if not found.
    :rtype: :class:`dict`
    '''

    warnings.warn(
        "Direct calls to paper() will be disabled in the future." +
        " Create an instance of SemanticScholar class instead.",
        DeprecationWarning)

    sch = SemanticScholar(timeout, api_key, api_url)

    return sch.paper(id, include_unknown_references)


def author(id, timeout: int=2, api_key: str=None, api_url: str=None) -> dict:
    '''Author lookup

    :param str id: S2AuthorId.
    :param float timeout: an exception is raised
        if the server has not issued a response for timeout seconds.
    :param str api_key: (optional) private API key.
    :param str api_url: (optional) custom API url.
    :returns: author data or empty :class:`dict` if not found.
    :rtype: :class:`dict`
    '''

    warnings.warn(
        "Direct calls to author() will be disabled in the future." +
        " Create an instance of SemanticScholar class instead.",
        DeprecationWarning)

    sch = SemanticScholar(timeout, api_key, api_url)

    return sch.author(id)
