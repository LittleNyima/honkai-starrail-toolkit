import copy
from typing import Dict

import qfluentwidgets as qfw
from PySide6 import QtWidgets
from PySide6.QtCore import QEvent, Qt, QUrl, Signal
from PySide6.QtGui import QColor, QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from qfluentwidgets.components.dialog_box import mask_dialog_base

from starrail.gui.common.stylesheet import StyleSheet
from starrail.utils import babelfish

AF = Qt.AlignmentFlag


class CheckUpdateDialog(mask_dialog_base.MaskDialogBase):

    cancelSignal = Signal()
    ndSignal = Signal()
    ghSignal = Signal()

    def __init__(
        self,
        title: str,
        content: str,
        parent: QtWidgets.QWidget = None,
        dist: Dict[str, str] = dict(),
    ):
        super().__init__(parent=parent)
        self.dist = copy.deepcopy(dist)

        self.__setupUi(title, content, self.widget)
        self.__initQss()
        self.__initLayout()
        self.__initWidget()

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, AF.AlignCenter)

        self.buttonGroup.setMinimumWidth(200)
        self.widget.setFixedSize(
            max(self.contentLabel.width(), self.titleLabel.width(), 150) + 48,
            self.contentLabel.y() + self.contentLabel.height() + 105,
        )
        self.__adjustText()

    def __setupUi(self, title, content, parent):
        self.title = title
        self.content = content
        self.titleLabel = QLabel(title, parent)
        self.contentLabel = QLabel(content, parent)

        self.buttonGroup = QtWidgets.QFrame(parent)
        if self.dist is not None:
            cancelText = babelfish.ui_cancel_update()
            ndText = babelfish.translate('netdisk_dist')
            ghText = babelfish.translate('GitHub_dist')
        else:
            cancelText = babelfish.ui_not_good()
            ndText = babelfish.ui_fine1()
            ghText = babelfish.ui_fine2()
        self.cancelButton = QPushButton(cancelText, self.buttonGroup)
        self.ndButton = qfw.PrimaryPushButton(ndText, self.buttonGroup)
        self.ghButton = qfw.PrimaryPushButton(ghText, self.buttonGroup)

        self.vBoxLayout = QVBoxLayout(parent)
        self.textLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout(self.buttonGroup)

    def __initWidget(self):
        self.cancelButton.setAttribute(
            Qt.WidgetAttribute.WA_LayoutUsesWidgetRect,
        )
        self.ndButton.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)
        self.ghButton.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)

        self.cancelButton.setFocus()
        self.buttonGroup.setFixedHeight(81)
        self.__adjustText()

        self.cancelButton.clicked.connect(self.onCancelClicked)
        self.ndButton.clicked.connect(self.onNdClicked)
        self.ghButton.clicked.connect(self.onGhClicked)

    def __initLayout(self):
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.textLayout, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, AF.AlignBottom)
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        self.textLayout.setSpacing(12)
        self.textLayout.setContentsMargins(24, 24, 24, 24)
        self.textLayout.addWidget(self.titleLabel, 0, AF.AlignTop)
        self.textLayout.addWidget(self.contentLabel, 0, AF.AlignTop)

        self.buttonLayout.setSpacing(12)
        self.buttonLayout.setContentsMargins(24, 24, 24, 24)
        self.buttonLayout.addWidget(self.cancelButton, 1, AF.AlignVCenter)
        self.buttonLayout.addWidget(self.ndButton, 1, AF.AlignVCenter)
        self.buttonLayout.addWidget(self.ghButton, 1, AF.AlignVCenter)

    def __initQss(self):
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        self.buttonGroup.setObjectName('buttonGroup')
        self.cancelButton.setObjectName('cancelButton')

        StyleSheet.CHECK_UPDATE_DIALOG.apply(self)

        self.cancelButton.adjustSize()
        self.ghButton.adjustSize()
        self.ndButton.adjustSize()

    def __adjustText(self):
        if self.isWindow():
            if self.parent():
                w = max(self.titleLabel.width(), self.parent().width())
                chars = max(min(w / 9, 140), 30)
            else:
                chars = 100
        else:
            w = max(self.titleLabel.width(), self.window().width())
            chars = max(min(w / 9, 100), 30)

        self.contentLabel.setText(
            qfw.TextWrap.wrap(self.content, chars, False)[0],
        )

    def onCancelClicked(self):
        self.reject()

    def onGhClicked(self):
        self.accept()
        if self.dist is not None and self.dist['GitHub_dist']:
            QDesktopServices.openUrl(QUrl(self.dist['GitHub_dist']))

    def onNdClicked(self):
        self.accept()
        if self.dist is not None and self.dist['netdisk_dist']:
            QDesktopServices.openUrl(QUrl(self.dist['netdisk_dist']))

    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self.__adjustText()

        return super().eventFilter(obj, e)
