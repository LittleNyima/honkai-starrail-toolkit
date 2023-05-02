import logging
import os

from starrail import package_path


def setup_logging(log_level):
    format = (
        '%(asctime)s %(name)s Line %(lineno)d - '
        '[%(levelname)s] %(message)s'
    )
    formatter = logging.Formatter(format)

    stream = logging.StreamHandler()
    stream.setFormatter(formatter)
    logging.getLogger().addHandler(stream)
    logging.getLogger().setLevel(log_level)


def get_logger(name):
    if name and os.path.isfile(name):
        name = os.path.relpath(name, package_path)
    return logging.getLogger(name)
