import copy
from enum import Enum
from typing import Dict

import qfluentwidgets as qfw
from PySide6 import QtWidgets
from PySide6.QtCore import QEvent, Qt, QUrl, Signal
from PySide6.QtGui import QColor, QDesktopServices, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from qfluentwidgets.components.dialog_box import mask_dialog_base

from starrail.gui.common.stylesheet import StyleSheet
from starrail.gui.widgets.button import DangerousPushButton
from starrail.mihoyo.qrcode import QrcodeStatus
from starrail.utils import babelfish
from starrail.utils.misc import create_qrcode_image

AF = Qt.AlignmentFlag


class DialogMode(Enum):

    OK = 'ok'

    OK_CANCEL = 'ok_cancel'

    DANGEROUS_OK_CANCEL = 'dangerous_ok_cancel'


class MaskDialog(mask_dialog_base.MaskDialogBase):

    okSignal = Signal()
    cancelSignal = Signal()

    def __init__(
        self,
        title: str,
        content: str,
        mode: DialogMode = DialogMode.OK_CANCEL,
        parent: QtWidgets.QWidget = None,
    ):
        super().__init__(parent=parent)

        self.__setupUi(title, content, self.widget)
        self.__initButtons(mode=mode)
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
        self.vBoxLayout = QVBoxLayout(parent)
        self.textLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout(self.buttonGroup)

    def __initButtons(self, mode: DialogMode):
        if mode == DialogMode.OK:
            self.okButton = qfw.PrimaryPushButton(
                babelfish.ui_ok(),
                self.buttonGroup,
            )
            self.cancelButton = None
            self.buttonLayout.addWidget(self.okButton, 1, AF.AlignVCenter)
        elif mode == DialogMode.OK_CANCEL:
            self.okButton = qfw.PrimaryPushButton(
                babelfish.ui_ok(),
                self.buttonGroup,
            )
            self.cancelButton = QPushButton(
                babelfish.ui_cancel(),
                self.buttonGroup,
            )
            self.buttonLayout.addWidget(self.okButton, 1, AF.AlignVCenter)
            self.buttonLayout.addWidget(self.cancelButton, 1, AF.AlignVCenter)
        elif mode == DialogMode.DANGEROUS_OK_CANCEL:
            self.okButton = DangerousPushButton(self.buttonGroup)
            self.okButton.setText(babelfish.ui_ok())
            self.cancelButton = QPushButton(
                babelfish.ui_cancel(),
                self.buttonGroup,
            )
            self.buttonLayout.addWidget(self.okButton, 1, AF.AlignVCenter)
            self.buttonLayout.addWidget(self.cancelButton, 1, AF.AlignVCenter)
        else:
            raise ValueError(f'Invalid dialog mode: {mode}')

    def __initQss(self):
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        self.buttonGroup.setObjectName('buttonGroup')
        if self.cancelButton:
            self.cancelButton.setObjectName('cancelButton')
        if self.okButton:
            self.okButton.setObjectName('okButton')

        StyleSheet.MASK_DIALOG.apply(self)

        if self.cancelButton:
            self.cancelButton.adjustSize()
        if self.okButton:
            self.okButton.adjustSize()

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

    def __initWidget(self):
        if self.cancelButton:
            self.cancelButton.setFocus()
        elif self.okButton:
            self.okButton.setFocus()

        if self.cancelButton:
            self.cancelButton.setAttribute(
                Qt.WidgetAttribute.WA_LayoutUsesWidgetRect,
            )
            self.cancelButton.clicked.connect(self.onCancelClicked)
        if self.okButton:
            self.okButton.clicked.connect(self.onOkClicked)
        self.buttonGroup.setFixedHeight(81)
        self.__adjustText()

    def onOkClicked(self):
        self.okSignal.emit()
        self.accept()

    def onCancelClicked(self):
        self.cancelSignal.emit()
        self.reject()

    def __adjustText(self):
        pass

    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self.__adjustText()

        return super().eventFilter(obj, e)


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

    def __initQss(self):
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        self.buttonGroup.setObjectName('buttonGroup')
        self.cancelButton.setObjectName('cancelButton')

        StyleSheet.MASK_DIALOG.apply(self)

        self.cancelButton.adjustSize()
        self.ghButton.adjustSize()
        self.ndButton.adjustSize()

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

    def __adjustText(self):
        # if self.isWindow():
        #     if self.parent():
        #         w = max(self.titleLabel.width(), self.parent().width())
        #         chars = max(min(w / 9, 140), 30)
        #     else:
        #         chars = 100
        # else:
        #     w = max(self.titleLabel.width(), self.window().width())
        #     chars = max(min(w / 9, 100), 30)

        # self.contentLabel.setText(
        #     qfw.TextWrap.wrap(self.content, chars, False)[0],
        # )
        pass

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


class QrcodeLoginDialog(mask_dialog_base.MaskDialogBase):

    updateStatusSignal = Signal(QrcodeStatus)
    connectFinishSignal = Signal()
    updateMessageSignal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__setupUi(self.widget)
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
            self.statusLabel.y() + self.statusLabel.height() + 105,
        )

        self.updateStatusSignal.connect(self.updateStatusSlot)
        self.connectFinishSignal.connect(self.connectFinishSlot)
        self.updateMessageSignal.connect(self.updateMessageSlot)
        self.worker = None

    def __setupUi(self, parent):
        self.titleLabel = QLabel(babelfish.ui_connect_to_hoyolab(), parent)
        self.qrcodeLabel = QLabel(parent)
        self.contentLabel = QLabel(parent)
        self.statusLabel = QLabel(
            text=babelfish.ui_connect_status(babelfish.ui_waiting()),
            parent=parent,
        )

        self.buttonGroup = QtWidgets.QFrame(parent)
        self.cancelButton = QPushButton(babelfish.ui_cancel())
        self.finishButton = qfw.PrimaryPushButton(babelfish.ui_done())

        self.vBoxLayout = QVBoxLayout(parent)
        self.textLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout(self.buttonGroup)

    def __initQss(self):
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        self.statusLabel.setObjectName('contentLabel')
        self.buttonGroup.setObjectName('buttonGroup')
        self.cancelButton.setObjectName('cancelButton')

        StyleSheet.MASK_DIALOG.apply(self)

        self.finishButton.adjustSize()

    def __initLayout(self):
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.textLayout, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, AF.AlignBottom)
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        self.textLayout.setSpacing(12)
        self.textLayout.setContentsMargins(24, 24, 24, 24)
        self.textLayout.addWidget(self.titleLabel, 0, AF.AlignTop)
        self.textLayout.addWidget(
            self.qrcodeLabel, 0, AF.AlignHCenter | AF.AlignTop,
        )
        self.textLayout.addWidget(self.contentLabel, 0, AF.AlignTop)
        self.textLayout.addWidget(self.statusLabel, 0, AF.AlignTop)

        self.buttonLayout.setSpacing(12)
        self.buttonLayout.setContentsMargins(24, 24, 24, 24)
        self.buttonLayout.addWidget(self.cancelButton, 1, AF.AlignVCenter)
        self.buttonLayout.addWidget(self.finishButton, 1, AF.AlignVCenter)

    def __initWidget(self):
        self.finishButton.setAttribute(
            Qt.WidgetAttribute.WA_LayoutUsesWidgetRect,
        )
        self.finishButton.setFocus()
        self.buttonGroup.setFixedHeight(81)
        self.cancelButton.clicked.connect(self.onCancelClicked)
        self.finishButton.clicked.connect(self.onFinishClicked)
        self.finishButton.setEnabled(False)

    def onCancelClicked(self):
        self.worker.stop_event.set()
        self.reject()

    def onFinishClicked(self):
        self.worker.stop_event.set()
        self.accept()

    def refreshQrcode(self, url: str):
        pixmap = QPixmap()
        data = create_qrcode_image(data=url)
        pixmap.loadFromData(data)
        pixmap = pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
        self.qrcodeLabel.setPixmap(pixmap)

        self.updateStatusSignal.emit(QrcodeStatus.INITIAL)

    def updateStatusSlot(self, status: QrcodeStatus):
        mapping = {
            QrcodeStatus.INITIAL: babelfish.ui_html_bold(
                babelfish.ui_scan_init(),
            ),
            QrcodeStatus.SCANNED: babelfish.ui_html_bold(
                babelfish.ui_html_font_color(
                    babelfish.ui_scan_scanned(), color='#BBBB00',
                ),
            ),
            QrcodeStatus.CONFIRMED: babelfish.ui_html_bold(
                babelfish.ui_html_font_color(
                    babelfish.ui_scan_confirmed(), color='#00BB66',
                ),
            ),
        }
        status_text = mapping[status]
        instr_text = babelfish.ui_scan_code_instr(status_text)
        if status == QrcodeStatus.CONFIRMED:
            instr_text = instr_text + babelfish.ui_wait_for_connection()
        self.contentLabel.setText(instr_text)

    def connectFinishSlot(self):
        self.statusLabel.setText(
            babelfish.ui_connect_status(babelfish.ui_connect_finish()),
        )
        self.cancelButton.setEnabled(False)
        self.finishButton.setEnabled(True)

    def updateMessageSlot(self, status: str):
        self.statusLabel.setText(babelfish.ui_connect_status(status))
