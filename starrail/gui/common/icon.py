from enum import Enum

from qfluentwidgets import FluentIconBase, Theme, getIconColor


class Icon(FluentIconBase, Enum):

    FILE_IMPORT = 'FileImport'
    UNLOCK = 'Unlock'
    USER = 'User'

    def path(self, theme=Theme.AUTO):
        return f'resources/svg/{self.value}_{getIconColor(theme)}.svg'
