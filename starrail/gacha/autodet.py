import configparser
import functools
import importlib
import os
import platform
import re
from urllib.parse import parse_qsl, urlparse

from starrail.utils import loggings

logger = loggings.get_logger(__file__)


reg_key_prefix = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\'
reg_key_cn = reg_key_prefix + '崩坏：星穹铁道'
# reg_key_os = reg_key_prefix + 'Star Rail'
api_pattern = re.compile(r'https://.+/api/getGachaLog.+game_biz=hkrpg.+')


@functools.lru_cache()
def lazyload(module_name):
    return importlib.import_module(module_name)


def detect_game_install_path():
    logger.info('Detecting game install path')
    winreg = lazyload('winreg')
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_key_cn) as rk:
        install_path = winreg.QueryValueEx(rk, 'InstallPath')[0]
    config_path = os.path.join(install_path, 'config.ini')
    parser = configparser.ConfigParser()
    parser.read(config_path)
    game_install_path = parser.get('launcher', 'game_install_path')
    if not os.path.exists(game_install_path):
        error_msg = (
            f'Game install path {game_install_path} is not existing. '
            'Please check whether the game is installed correctly.'
        )
        logger.error(error_msg)
    return game_install_path


def get_cache_path(game_install_path):
    logger.info('Getting gacha query cache path')
    cache_path = os.path.join(
        game_install_path, 'StarRail_Data', 'webCaches',
        'Cache', 'Cache_Data', 'data_2',
    )
    if not os.path.exists(cache_path):
        error_msg = (
            f'Cache path {cache_path} is not existing. Please visit '
            'the gacha querying page before exporting gacha data.'
        )
        logger.error(error_msg)
    return cache_path


def get_url_from_text(text):
    if not text:
        return None
    urls = re.findall(api_pattern, text)
    if not urls:
        return None
    return urls[-1]


def safe_int(value, default_value=0):
    try:
        return int(value)
    except Exception:
        return default_value


def get_timestamp_from_url(url):
    parse = urlparse(url)
    query_dict = dict(parse_qsl(parse.query))
    timestamp = query_dict.get('timestamp', 0)
    return safe_int(timestamp)


def get_latest_url(url_list):
    timestamp_list = list(map(get_timestamp_from_url, url_list))
    max_timestamp = max(timestamp_list)
    max_index = [
        idx for idx, timestamp in enumerate(timestamp_list)
        if timestamp == max_timestamp
    ]
    return url_list[max_index[-1]]


# Modified from: https://github.com/sunfkny/genshin-gacha-export
def get_api_from_cache(cache_path):
    logger.info('Getting api URL from cache')
    with open(cache_path, 'rb') as f_cache:
        cache = f_cache.read()
    parts = cache.split(b'1/0/')
    parts = [part.split(b'\x00')[0].decode(errors='ignore') for part in parts]
    parts = map(get_url_from_text, parts)
    parts = list(filter(bool, parts))
    if not parts:
        error_msg = (
            'API URL is not found in cache. Please visit the gacha querying '
            'page before exporting gacha data.'
        )
        logger.error(error_msg)
        return ''
    return get_latest_url(parts)


def detect_api_url():
    if platform.system() == 'Windows':
        logger.info('Trying to auto-detecting API URL')
        game_install_path = detect_game_install_path()
        cache_path = get_cache_path(game_install_path)
        return get_api_from_cache(cache_path)
    else:
        logger.error(
            'Auto-detect API URL is only supported on Windows '
            'platform, aborting.',
        )
