"""Config for graphic mode used by starrail package.

This configurataion overrides starrail.config, and should be compatible with
that one. The global configuration is read-only in graphic mode.
"""

import os
from pathlib import Path

import qfluentwidgets
from qfluentwidgets import BoolValidator, ConfigItem

userroot = os.path.abspath(os.path.expanduser('~'))


class StarRailConfig(qfluentwidgets.QConfig):

    cache_dir = os.path.join(userroot, '.starrail')
    db_dir = os.path.join(userroot, '.starrail', 'database')
    config_path = os.path.join(userroot, '.starrail', 'qconfig.json')

    check_update = ConfigItem(
        group='StarRailToolkit',
        name='CheckUpdate',
        default=True,
        validator=BoolValidator(),
        restart=False,
    )

    def __init__(self, path):
        super().__init__()
        self.file = Path(path)


qcfg = StarRailConfig(path=StarRailConfig.config_path)
qfluentwidgets.qconfig.load(StarRailConfig.config_path)
