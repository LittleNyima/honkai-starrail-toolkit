__version__ = '0.7.0'


def digital_version(version: str):
    return tuple(map(int, version.split('.')))
