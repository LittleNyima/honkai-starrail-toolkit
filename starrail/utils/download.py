import os
import traceback
from typing import Tuple
from urllib.parse import urlparse

import requests

from starrail.config import configuration as cfg
from starrail.utils import loggings
from starrail.utils.misc import sha1

logger = loggings.get_logger(__file__)


def get_filename_from_url(url: str) -> str:
    path = urlparse(url).path
    return os.path.basename(path)


def download(url: str, cached: bool = True) -> Tuple[bytes, str]:
    hash = sha1(url)
    max_length = 127 - 1 - len(hash)
    filename = get_filename_from_url(url)
    if len(filename) > max_length:
        start = len(filename) - max_length
        filename = filename[start:]
    cache_path = os.path.join(cfg.res_cache_dir, f'{hash}_{filename}')

    if cached and os.path.isfile(cache_path):
        with open(cache_path, 'rb') as fin:
            data = fin.read()
        return data, cache_path

    try:
        r = requests.get(url, timeout=5)
        if 200 <= r.status_code < 300:
            with open(cache_path, 'wb') as fout:
                fout.write(r.content)
            return r.content, cache_path
    except Exception:
        logger.error(traceback.format_exc())

    if os.path.isfile(cache_path):  # fallback to cache
        with open(cache_path, 'rb') as fin:
            data = fin.read()
        return data, cache_path
    return b'', ''
