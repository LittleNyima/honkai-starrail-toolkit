__version__ = '0.6.4'


def digital_version(version: str):
    return tuple(map(int, version.split('.')))
