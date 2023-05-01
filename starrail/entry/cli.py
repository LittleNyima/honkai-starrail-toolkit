import argparse

from starrail.config import configuration as cfg
from starrail.config import init_config
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
        choices=['all', 'json', 'xlsx', 'csv', 'md'],  # TODO: html
        help='Types of expected export formats.',
    )

    return parser.parse_args()


def cli_entry():
    setup()
    args = parse_args()
    init_config(cli=True)
    logger.info(args)
    logger.info(cfg)
    export_gacha_from_api(api_url=args.api, export=args.export)
