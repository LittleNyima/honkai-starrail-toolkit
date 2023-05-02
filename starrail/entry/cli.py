import argparse

from starrail.config import configuration as cfg
from starrail.entry.setup import setup
from starrail.gacha.service import export_gacha_from_api
from starrail.utils import loggings

logger = loggings.get_logger(__file__)


def parse_args():
    parser = argparse.ArgumentParser(
        prog='hksr',
        description='Honkai: Star Rail Toolkit',
    )
    parser.add_argument(
        '--api', type=str,
        help='URL of the gacha api, please refer to README.md for details.',
    )
    parser.add_argument(
        '--export', nargs='+', type=str,
        choices=['all', 'csv', 'html', 'json', 'md', 'xlsx'],
        help='Types of expected export formats.',
    )
    parser.add_argument(
        '--locale', type=str, default='zhs',
        choices=['en', 'zhs'],
        help=(
            'Language of gacha report. Abbreviations: `en` for English, '
            '`zhs` for simplified Chinese'
        ),
    )
    parser.add_argument(
        '--log-level', type=str, default='DEBUG',
        choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG'],
        help='Controlling the level of logging output.',
    )

    return parser.parse_args()


def cli_entry():
    args = parse_args()
    setup(log_level=args.log_level)
    logger.info(args)
    logger.info(cfg)
    export_gacha_from_api(api_url=args.api, export=args.export)
