import os

from .version import __version__

package_path = os.path.dirname(__file__)

__all__ = ['__version__', 'package_path']
