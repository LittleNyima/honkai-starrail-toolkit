from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    BASE_INTERFACE = 'base_interface'
    CHECK_UPDATE_DIALOG = 'check_update_dialog'
    HOME_INTERFACE = 'home_interface'
    LINK_CARD = 'link_card'
    RESULT_TABLE_WIDGET = 'result_table_widget'
    SETTING_INTERFACE = 'setting_interface'
    STAR_RAIL_TOOLKIT = 'star_rail_toolkit'

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f'resources/qss/{theme.value.lower()}/{self.value}.qss'
