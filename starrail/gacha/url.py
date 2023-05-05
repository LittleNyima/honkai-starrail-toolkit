from typing import Dict, List, Optional
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from starrail.utils import loggings

logger = loggings.get_logger(__file__)
QueryDictType = Dict[str, List[str]]


def get_clean_query_dict(query_dict: QueryDictType) -> QueryDictType:
    """
    Given a dictionary of query parameters, remove any backslashes in the
    keys and values and return a new dictionary with the cleaned keys and
    values.

    Args:
        query_dict (QueryDictType): A dictionary containing query parameters

    Returns:
        QueryDictType: A new dictionary with the cleaned keys and values
    """

    clean_query = dict()
    for k, v in query_dict.items():
        clean_k = k.replace('\\', '')
        clean_v = [item.replace('\\', '') for item in v]
        clean_query[clean_k] = clean_v
    return clean_query


def pop_if_exist(query_dict: QueryDictType, key: str) -> Optional[List[str]]:
    """
    Given a dictionary of query parameters and a key, remove the key from the
    dictionary if it exists and return its corresponding value. If the key
    does not exist, return None.

    Args:
        query_dict (QueryDictType): A dictionary containing query parameters
        key (str): The key to remove from the dictionary

    Returns:
        Optional[str]: The corresponding value of the key that was removed,
            or None if the key did not exist
    """

    if key in query_dict:
        return query_dict.pop(key)
    return None


def get_url_template(url: str) -> str:
    """
    Given a URL string, remove specific query parameters
    ('end_id', 'gacha_type', 'page', 'size'),
    remove any backslashes from the remaining query parameters,
    and return a new URL string with the cleaned query parameters.

    Args:
        url (str): A URL string containing query parameters

    Returns:
        str: A new URL string with the cleaned query parameters
    """

    parse = urlparse(url)
    query_dict = parse_qs(parse.query)
    query_dict = get_clean_query_dict(query_dict)
    pop_if_exist(query_dict, 'begin_id')
    pop_if_exist(query_dict, 'end_id')
    pop_if_exist(query_dict, 'gacha_type')
    pop_if_exist(query_dict, 'page')
    pop_if_exist(query_dict, 'size')
    new_query = urlencode(query_dict, doseq=True)
    return urlunparse((
        parse.scheme, parse.netloc, parse.path, parse.params,
        new_query, parse.fragment,
    ))


def get_api_url(
    template: str, end_id: str, gacha_type: str, page: str,
    size: str,
) -> str:
    """
    Constructs and returns an API URL based on the given template and
    parameters.

    Args:
        template (str): The base URL template to be used as a starting point.
        end_id (str): The ending ID for the desired data range.
        gacha_type (str): The type of gacha data to retrieve.
        page (str): The page number of results to return.
        size (str): The number of results per page to return.

    Returns:
        str: A string representing the complete API URL with all necessary
            parameters included.
    """

    parse = urlparse(template)
    query_dict = parse_qs(parse.query)
    query_dict.update({
        'end_id': [end_id],
        'gacha_type': [gacha_type],
        'page': [page],
        'size': [size],
    })
    new_query = urlencode(query_dict, doseq=True)
    return urlunparse((
        parse.scheme, parse.netloc, parse.path, parse.params,
        new_query, parse.fragment,
    ))
