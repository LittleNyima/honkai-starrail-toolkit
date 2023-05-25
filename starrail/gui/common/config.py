"""Config for graphic mode used by starrail package.

This configurataion overrides starrail.config, and should be compatible with
that one. The global configuration is read-only in graphic mode.
"""

import os
from enum import Enum
from pathlib import Path

import qfluentwidgets as qfw
from PySide6.QtCore import QLocale

userroot = os.path.abspath(os.path.expanduser('~'))


class Language(Enum):

    AUTO = QLocale()
    CHINESE_SIMPLIFIED = QLocale(
        QLocale.Language.Chinese,
        QLocale.Country.China,
    )
    ENGLISH = QLocale(
        QLocale.Language.English,
        QLocale.Country.UnitedStates,
    )


class LanguageSerializer(qfw.ConfigSerializer):

    def serialize(self, language: Language):
        return language.value.name() if language != Language.AUTO else 'auto'

    def deserialize(self, value):
        return Language(QLocale(value)) if value != 'auto' else Language.AUTO


class StarRailConfig(qfw.QConfig):

    cache_dir = os.path.join(userroot, '.starrail')
    db_dir = os.path.join(userroot, '.starrail', 'database')
    config_path = os.path.join(userroot, '.starrail', 'qconfig.json')

    locale = qfw.OptionsConfigItem(
        group='StarRailToolkit',
        name='Locale',
        default=Language.CHINESE_SIMPLIFIED,
        validator=qfw.OptionsValidator(Language),
        serializer=LanguageSerializer(),
        restart=True,
    )

    check_update = qfw.ConfigItem(
        group='StarRailToolkit',
        name='CheckUpdate',
        default=True,
        validator=qfw.BoolValidator(),
        restart=False,
    )

    def __init__(self, path):
        super().__init__()
        self.file = Path(path)
        if not self.file.exists():
            self.set(self.themeColor, '#ff0077dd')
            self.set(self.themeMode, qfw.Theme.DARK)


qcfg = StarRailConfig(path=StarRailConfig.config_path)
qfw.qconfig.load(StarRailConfig.config_path, qcfg)
