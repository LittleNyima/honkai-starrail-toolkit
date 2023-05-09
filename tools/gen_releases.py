import json

import starrail
from starrail.utils import babelfish

releases = r'https://github.com/LittleNyima/honkai-starrail-toolkit/releases'


def valid_info(dist_info):
    print('version:')
    print(f' * {dist_info["version"]}')
    print('dist:')
    for key, value in dist_info['dist'].items():
        print(f' * {babelfish.translate(key)}: {value}')
    print('changelog:')
    print(dist_info['changelog'])


if __name__ == '__main__':
    with open('releases/changelog.txt', encoding='utf-8') as changelog:
        dist_info = {
            'version': starrail.__version__,
            'dist': {
                'GitHub_dist': releases,
                'netdisk_dist': '',
            },
            'changelog': changelog.read().strip(),
        }
    with open('releases/dist.json', 'w', encoding='utf-8') as f:
        json.dump(dist_info, f, ensure_ascii=False, indent=2)
    valid_info(dist_info)
