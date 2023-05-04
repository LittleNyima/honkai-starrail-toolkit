import json
import traceback

import requests

from starrail.utils import loggings

logger = loggings.get_logger(__file__)


def fetch_json(url):  # no typing annotations to pass mypy check
    """
    Fetches JSON content from a URL and returns it as a dictionary.

    Args:
        url: A string representing the URL to fetch the JSON content from.

    Returns:
        A dictionary representing the JSON content fetched from the URL.
    """

    try:
        r = requests.get(url)
        if 200 <= r.status_code < 300:
            content = r.content.decode('utf-8')
            payload = json.loads(content)
            logger.debug(json.dumps(payload, ensure_ascii=False, indent=2))
            return payload, r.status_code
    except Exception:
        traceback.print_exc()
    return None, -1
