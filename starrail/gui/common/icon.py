from enum import Enum

from qfluentwidgets import FluentIconBase, Theme, getIconColor


class Icon(FluentIconBase, Enum):

    USER = 'User'

    def path(self, theme=Theme.AUTO):
        return f'resources/images/icons/{self.value}_{getIconColor(theme)}.svg'
