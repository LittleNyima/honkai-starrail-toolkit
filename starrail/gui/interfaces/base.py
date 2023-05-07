import qfluentwidgets as qfw
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from starrail.gui.common.stylesheet import StyleSheet

AF = Qt.AlignmentFlag


class ToolBar(QWidget):

    def __init__(self, title, subtitle, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = QLabel(title, self)
        self.subtitleLabel = QLabel(subtitle, self)

        self.vBoxLayout = QVBoxLayout(self)

        self.__initWidget()

    def __initWidget(self):
        self.setFixedHeight(98)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(36, 22, 12, 12)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addWidget(self.subtitleLabel)
        self.vBoxLayout.setAlignment(AF.AlignTop)

        self.titleLabel.setObjectName('titleLabel')
        self.subtitleLabel.setObjectName('subtitleLabel')


class BaseInterface(qfw.ScrollArea):

    def __init__(self, title: str, subtitle: str, parent: QWidget = None):
        super().__init__(parent=parent)
        self.view = QWidget(self)
        self.toolBar = ToolBar(title, subtitle, self)
        self.vBoxLayout = QVBoxLayout(self.view)

        SBP = Qt.ScrollBarPolicy
        self.setHorizontalScrollBarPolicy(SBP.ScrollBarAlwaysOff)
        self.setViewportMargins(0, self.toolBar.height(), 0, 0)
        self.setWidget(self.view)
        self.setWidgetResizable(True)

        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.setAlignment(AF.AlignTop)
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)

        self.view.setObjectName('view')
        StyleSheet.BASE_INTERFACE.apply(self)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.toolBar.resize(self.width(), self.toolBar.height())
