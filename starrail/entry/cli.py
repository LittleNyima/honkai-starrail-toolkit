import argparse
import traceback

from starrail import __version__, digital_version
from starrail.config import configuration as cfg
from starrail.entry.setup import setup
from starrail.gacha.service import export_gacha_from_api, import_srgf_data
from starrail.unlock.service import unlock_fps
from starrail.utils import babelfish, loggings
from starrail.utils.auto_update import check_update

logger = loggings.get_logger(__file__)


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='hksr',
        description='Honkai: Star Rail Toolkit',
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

    subparsers = parser.add_subparsers(dest='command')

    gacha = subparsers.add_parser('gacha')
    gacha.add_argument(
        '--api', type=str,
        help='URL of the gacha api, please refer to README.md for details.',
    )
    gacha.add_argument(
        '--export', nargs='+', type=str, default=['all'],
        choices=['all', 'csv', 'html', 'json', 'md', 'srgf', 'xlsx'],
        help='Types of expected export formats.',
    )
    gacha.add_argument(
        '--load', type=str,
        help='Import source json under SRGF standard.',
    )
    gacha.add_argument(
        '--request-interval', type=float, default=0.1,
        help='Minimum interval (seconds) between two requests.',
    )

    unlock = subparsers.add_parser('unlock')
    unlock.add_argument(
        '--fps', type=int,
        help='Target FPS of the game',
    )
    unlock.add_argument(
        '--reset', action='store_true',
        help='Reset FPS to the initial value',
    )

    return parser


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
                logger.info('Your program is the latest version.')
        except Exception:
            logger.warning(
                'Check update failed. '
                'Please check your network connection.',
            )


def cli_entry():
    parser = get_parser()
    args = parser.parse_args()
    setup(log_level=args.log_level, locale=args.locale)
    logger.info(args)
    logger.info(cfg)
    cli_check_update()

    if args.command == 'gacha':
        import_srgf_data(filename=args.load)
        export_gacha_from_api(
            api_url=args.api,
            export=args.export,
            request_interval=args.request_interval,
        )
    elif args.command == 'unlock':
        unlock_fps(fps=args.fps, reset=args.reset)
    else:
        parser.print_help()


if __name__ == '__main__':
    try:
        cli_entry()
    except Exception:
        traceback.print_exc()
    finally:
        input('Press `Enter` to exit.')
