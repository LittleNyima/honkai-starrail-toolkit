import json
import platform

from starrail.utils import loggings
from starrail.utils.misc import lazy_import

logger = loggings.get_logger(__file__)


fps_reg_key_cn = 'Software\\miHoYo\\崩坏：星穹铁道'


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
            key_name = [
                x for x in winreg.QueryValueEx(rk, '')[1]
                if x.startswith('GraphicsSettings_Model')
            ][0]
            key = winreg.QueryValueEx(rk, key_name)[0]
            reg_value = key.decode('utf-8')
            json_data = json.loads(reg_value)
            json_data['FPS'] = value
            new_value = json.dumps(json_data).encode('utf-8')
            winreg.SetValueEx(rk, key_name, 0, winreg.REG_BINARY, new_value)
    else:
        logger.error(
            'Setting FPS is only supported on Windows platform, aborting.',
        )
