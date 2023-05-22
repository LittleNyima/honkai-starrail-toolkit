import qfluentwidgets as qfw
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

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


class CardWidget(QWidget):

    def __init__(self, title, parent=None):
        super().__init__(parent=parent)

        self.titleLabel = QLabel(title, self)
        self.card = QtWidgets.QFrame(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = QVBoxLayout(self.card)
        self.topLayout = QHBoxLayout()

        self.__initLayout()
        self.__initWidget()

    def __initWidget(self):
        self.titleLabel.setObjectName('titleLabel')
        self.card.setObjectName('card')

    def __initLayout(self):
        QVBL_SC = QVBoxLayout.SizeConstraint
        QHBL_SC = QHBoxLayout.SizeConstraint
        self.vBoxLayout.setSizeConstraint(QVBL_SC.SetMinimumSize)
        self.cardLayout.setSizeConstraint(QVBL_SC.SetMinimumSize)
        self.topLayout.setSizeConstraint(QHBL_SC.SetMinimumSize)

        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.setContentsMargins(12, 12, 12, 12)
        self.cardLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.titleLabel, 0, AF.AlignTop)
        self.vBoxLayout.addWidget(self.card, 0, AF.AlignTop)
        self.vBoxLayout.setAlignment(AF.AlignTop)

        self.cardLayout.setSpacing(0)
        self.cardLayout.setAlignment(AF.AlignTop)
        self.cardLayout.addLayout(self.topLayout, 0)

    def addWidget(self, widget: QWidget):
        widget.setParent(self.card)
        self.topLayout.addWidget(widget)
        widget.show()

    def addStretch(self, stretch: int):
        self.topLayout.addStretch(stretch)

    def addSpacing(self, spacing: int):
        self.topLayout.addSpacing(spacing)


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

    def addCard(self, title):
        card = CardWidget(title=title, parent=self)
        self.vBoxLayout.addWidget(card, 0, AF.AlignTop)
        return card

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.toolBar.resize(self.width(), self.toolBar.height())
