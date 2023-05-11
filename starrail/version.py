__version__ = '0.5.6'


def digital_version(version: str):
    return tuple(map(int, version.split('.')))
