import os

from .version import __version__

package_path = os.path.dirname(__file__)


def _welcome():
    print('+--------------------------------------+')
    print('|      Honkai: Star Rail Toolkit       |')
    print('|      ^^^^^^^^^^^^^^^^^^^^^^^^^       |')
    print('|         author: LittleNyima          |')
    print('+--------------------------------------+')
    print(
        'NOTICE: This software is licensed under the GNU General Public\n'
        'License v3.0 and SHALL NOT be used for commercial purpose. All\n'
        'rights reserved to LittleNyima. Please contact me if the project\n'
        'has any potential infringement risks.',
    )


_welcome()


__all__ = ['__version__', 'package_path']
