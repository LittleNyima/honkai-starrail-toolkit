import json
import platform

from starrail.utils import loggings
from starrail.utils.misc import lazy_import

logger = loggings.get_logger(__file__)


fps_reg_key_cn = 'Software\\miHoYo\\崩坏：星穹铁道'
graphics_model = 'GraphicsSettings_Model_h2986158309'


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
    else:
        logger.error(
            'Setting FPS is only supported on Windows platform, aborting.',
        )


def safe_set_fps(value):
    try:
        set_fps(value)
        return True
    except Exception:
        logger.fatal(
            'Setting FPS is not success. Please first set FPS in '
            'game for one time and try again.',
        )
        return False
