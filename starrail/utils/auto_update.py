import easydict

from starrail.gacha.fetch import fetch_json

user = 'LittleNyima'
repo = 'honkai-starrail-toolkit'
branch = 'master'
cdn_templ = dict(
    gitee=fr'https://gitee.com/{user}/{repo}-mirror/raw/{branch}/',
    github=fr'https://raw.githubusercontent.com/{user}/{repo}/{branch}/',
    jsdelivr=fr'https://cdn.jsdelivr.net/gh/{user}/{repo}@{branch}/',
)
# jsdelivr is deprecated due to untimely synchronization


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


def get_distribution(cdn_type):
    distribution = fr'{cdn_templ[cdn_type]}releases/dist.json'
    return fetch_json(distribution)


def check_update():
    for cdn_type in ['github', 'gitee']:
        payload, _ = get_distribution(cdn_type)
        if payload is not None:
            return easydict.EasyDict(payload)
    return None
