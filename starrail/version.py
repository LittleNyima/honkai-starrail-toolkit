__version__ = '0.6.2'


def digital_version(version: str):
    return tuple(map(int, version.split('.')))
