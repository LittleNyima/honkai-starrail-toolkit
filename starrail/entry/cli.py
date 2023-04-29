import argparse
import logging

from starrail.config import configuration as cfg
from starrail.config import init_config
from starrail.gacha.service import export_gacha_from_api


def parse_args():
    parser = argparse.ArgumentParser(
        prog='starrail',
        description='Honkai: Star Rail Toolkit',
    )
    parser.add_argument(
        'api', type=str, required=True,
        help='URL of the gacha api, please refer to README.md for details.',
    )
    parser.add_argument(
        '--uid', type=str, help='UID, required if multi-user is preferred.',
    )
    parser.add_argument(
        '--export', nargs='+', type=str,
        choices=['all', 'json', 'xslx', 'csv', 'html'],
        help='Types of expected export formats.',
    )

    return parser.parse_args()


def cli_entry():
    args = parse_args()
    logging.info(args)
    init_config(cli=True)
    logging.info(cfg)
    export_gacha_from_api(api_url=args.api, uid=args.uid)
