from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    ANNOUNCEMENT = 'announcement'
    BASE_INTERFACE = 'base_interface'
    BUTTON = 'button'
    GACHA_RECORD = 'gacha_record'
    HOME_INTERFACE = 'home_interface'
    LINK_CARD = 'link_card'
    MASK_DIALOG = 'mask_dialog'
    RESULT_TABLE_WIDGET = 'result_table_widget'
    SETTING_INTERFACE = 'setting_interface'
    STAR_RAIL_TOOLKIT = 'star_rail_toolkit'

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f'resources/qss/{theme.value.lower()}/{self.value}.qss'
