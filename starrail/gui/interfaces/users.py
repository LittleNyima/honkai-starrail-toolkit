from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from starrail.gui.interfaces.base import BaseInterface


class UsersInterface(BaseInterface):

    def __init__(self, title, subtitle, parent):
        super().__init__(title, subtitle, parent)
        self.vBoxLayout.addWidget(
            QLabel('coming soon'), 0, Qt.AlignmentFlag.AlignTop,
        )
