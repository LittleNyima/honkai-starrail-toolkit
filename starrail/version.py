__version__ = '0.6.3'


def digital_version(version: str):
    return tuple(map(int, version.split('.')))
