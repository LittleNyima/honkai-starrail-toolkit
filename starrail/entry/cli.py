import argparse
import traceback

from starrail import __version__, digital_version
from starrail.config import configuration as cfg
from starrail.entry.setup import setup
from starrail.gacha.service import export_gacha_from_api
from starrail.utils import babelfish, loggings
from starrail.utils.auto_update import check_update

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
        '--export', nargs='+', type=str, default=['all'],
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
    parser.add_argument(
        '--request-interval', type=float, default=0.1,
        help='Minimum interval (seconds) between two requests.',
    )

    return parser.parse_args()


def cli_check_update():
    if cfg.check_update:
        try:
            latest = check_update()
            logger.info('Check Update:')
            logger.info(f' * Current version is {__version__}')
            logger.info(f' * Latest release version is {latest.version}')
            if digital_version(__version__) < digital_version(latest.version):
                cmd = 'pip install starrail-toolkit -U --force-reinstall'
                logger.info('New version of package is available.')
                logger.info(
                    f'If you use cli, please update with pip: `f{cmd}`',
                )
                logger.info('If you use GUI, please download executables:')
                for name, url in latest.dist.items():
                    logger.info(f' * {babelfish.translate(name)}: {url}')
            else:
                logger.info('No update is required.')
        except Exception:
            logger.warning(
                'Check update failed. '
                'Please check your network connection.',
            )


def cli_entry():
    args = parse_args()
    setup(log_level=args.log_level, locale=args.locale)
    logger.info(args)
    logger.info(cfg)
    cli_check_update()
    export_gacha_from_api(
        api_url=args.api,
        export=args.export,
        request_interval=args.request_interval,
    )


if __name__ == '__main__':
    try:
        cli_entry()
    except Exception:
        traceback.print_exc()
    finally:
        input('Press `Enter` to exit.')
