import qfluentwidgets as qfw
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout

from starrail.gui.interfaces.base import BaseInterface
from starrail.utils import babelfish

AF = Qt.AlignmentFlag


class GachaSyncInterface(BaseInterface):

    def __init__(self, title, subtitle, parent):
        super().__init__(title, subtitle, parent)

        self.buttonLayout = QHBoxLayout()
        self.syncButton = qfw.PrimaryPushButton(babelfish.ui_sync())

        self.__initWidget()

    def __initWidget(self):
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(AF.AlignLeft)
        self.buttonLayout.addWidget(self.syncButton)

        self.vBoxLayout.addLayout(self.buttonLayout)
