import json
import platform
import traceback

from starrail.utils import loggings
from starrail.utils.misc import lazy_import

logger = loggings.get_logger(__file__)


fps_reg_key_cn = 'Software\\miHoYo\\崩坏：星穹铁道'
graphics_model = 'GraphicsSettings_Model_h2986158309'


def get_fps():
    if platform.system() == 'Windows':
        winreg = lazy_import('winreg')
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            fps_reg_key_cn,
            0,
            winreg.KEY_READ,
        ) as rk:
            settings = winreg.QueryValueEx(rk, graphics_model)
            settings = settings[0].decode('utf-8').strip('\x00')
            settings = json.loads(settings)
            return settings['FPS']
    else:
        logger.error(
            'Getting FPS is only supported on Windows platform, aborting.',
        )
        return 60


def safe_get_fps(default_value=60):
    try:
        return get_fps()
    except Exception:
        return default_value


def set_fps(value):
    if platform.system() == 'Windows':
        logger.info(f'trying to set fps to {value}')
        winreg = lazy_import('winreg')
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            fps_reg_key_cn,
            0,
            winreg.KEY_ALL_ACCESS,
        ) as rk:
            settings = winreg.QueryValueEx(rk, graphics_model)
            settings = settings[0].decode('utf-8').strip('\x00')
            settings = json.loads(settings)
            settings['FPS'] = value
            settings = json.dumps(settings) + '\x00'
            settings = settings.encode('utf-8')
            winreg.SetValueEx(
                rk,
                graphics_model,
                0,
                winreg.REG_BINARY,
                settings,
            )
        logger.info(f'Successfully set FPS to {value}.')
        return True, 'ok'
    else:
        logger.error(
            'Setting FPS is only supported on Windows platform, aborting.',
        )
        return False, 'Platform not supported'


def safe_set_fps(value):
    try:
        return set_fps(value)
    except Exception:
        logger.fatal(
            'Setting FPS is not success. Please first set FPS in '
            'game for one time and try again.',
        )
        return False, traceback.format_exc()
