import platform

from starrail.config import init_config
from starrail.utils.babelfish.locale import setup_locale
from starrail.utils.loggings import get_logger, setup_logging

logger = get_logger(__file__)


def display_platform_info():
    logger.info(f'PLATFORM:     {platform.platform()}')
    logger.info(f'VERSION:      {platform.version()}')
    logger.info(f'ARCHITECTURE: {platform.architecture()}')
    logger.info(f'MACHINE:      {platform.machine()}')
    logger.info(f'NODE:         {platform.node()}')
    logger.info(f'PROCESSOR:    {platform.processor()}')
    logger.info(f'SYSTEM:       {platform.system()}')
    logger.info(f'RELEASE:      {platform.release()}')


def display_python_info():
    logger.info(f'PYTHON_BRANCH:         {platform.python_branch()}')
    logger.info(f'PYTHON_BUILD:          {platform.python_build()}')
    logger.info(f'PYTHON_COMPILER:       {platform.python_compiler()}')
    logger.info(f'PYTHON_IMPLEMENTATION: {platform.python_implementation()}')
    logger.info(f'PYTHON_REVISION:       {platform.python_revision()}')
    logger.info(f'PYTHON_VERSION:        {platform.python_version()}')


def setup(log_level, locale):
    setup_logging(log_level)
    setup_locale(locale)
    init_config()
    display_platform_info()
    display_python_info()
