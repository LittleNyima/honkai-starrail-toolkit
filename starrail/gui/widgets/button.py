import qfluentwidgets as qfw
from PySide6.QtWidgets import QWidget

from starrail.gui.common.stylesheet import StyleSheet


class DangerousPushButton(qfw.PushButton):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        qfw.StyleSheetCompose(
            [qfw.FluentStyleSheet.BUTTON, StyleSheet.BUTTON],
        ).apply(self)
