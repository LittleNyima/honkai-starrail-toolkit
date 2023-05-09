import easydict

from starrail.gacha.fetch import fetch_json

user = 'LittleNyima'
repo = 'honkai-starrail-toolkit'
branch = 'master'
cdn_templ = fr'https://cdn.jsdelivr.net/gh/{user}/{repo}@{branch}/'
# version = fr'{cdn_templ}releases/version.txt'
distribution = fr'{cdn_templ}releases/dist.json'


"""
Distribution JSON Format:
{
    'version': 'the-latest-version',
    'dist': {
        'name-1': 'url-1',
        'name-2': 'url-2',
    },
    'changelog': 'desc'
}
"""


def get_distribution():
    return fetch_json(distribution)


def check_update():
    payload, _ = get_distribution()
    if payload is not None:
        return easydict.EasyDict(payload)
    return None
