from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    STAR_RAIL_TOOLKIT = 'star_rail_toolkit'

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f'resources/qss/{theme.value.lower()}/{self.value}.qss'
