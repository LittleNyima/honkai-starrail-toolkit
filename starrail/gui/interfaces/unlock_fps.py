import qfluentwidgets as qfw
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QLabel

from starrail.gui.common.icon import Icon
from starrail.gui.interfaces.base import BaseInterface
from starrail.unlock.fps import safe_get_fps, safe_set_fps
from starrail.unlock.service import default_fps
from starrail.utils import babelfish


class SetFpsThread(QThread):

    successSignal = Signal(str)
    failureSignal = Signal(str)

    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.value = value

    def run(self):
        success, msg = safe_set_fps(self.value)
        if success:
            self.successSignal.emit(babelfish.ui_fps_is_set_to(self.value))
        else:
            self.failureSignal.emit(babelfish.ui_set_fps_fail_with_msg(msg))


class UnlockFpsInterface(BaseInterface):

    def __init__(self, title, subtitle, parent):
        super().__init__(title, subtitle, parent)
        self.settingCard = self.addCard(babelfish.ui_setting_panel())
        self.statusCard = self.addCard(babelfish.ui_status_panel())

        self.spinBox = qfw.SpinBox()
        self.settingButton = qfw.PrimaryPushButton(
            text=babelfish.ui_unlock_fps(),
            parent=self.settingCard,
            icon=Icon.UNLOCK,
        )
        self.settingButton.clicked.connect(self.__setFpsSlot)
        self.resetButton = qfw.PrimaryPushButton(
            text=babelfish.ui_reset_fps(),
            parent=self.settingCard,
            icon=qfw.FluentIcon.CANCEL,
        )
        self.resetButton.clicked.connect(self.__resetFpsSlot)
        self.currFpsLabel = QLabel(text=babelfish.ui_curr_fps(''))
        self.currFps = 60

        self.setFpsThread = None

        self.__initWidget()
        self.__initStatus()

    def __initWidget(self):
        self.spinBox.setRange(30, 240)
        self.spinBox.setSingleStep(30)
        self.spinBox.setValue(120)
        self.settingCard.addWidget(self.spinBox)
        self.settingCard.addSpacing(10)
        self.settingCard.addWidget(self.settingButton)
        self.settingCard.addSpacing(10)
        self.settingCard.addWidget(self.resetButton)
        self.settingCard.addStretch(1)

        self.statusCard.addWidget(self.currFpsLabel)
        self.statusCard.addStretch(1)

    def __initStatus(self):
        self.currFps = safe_get_fps()
        self.__setCurrFPS(self.currFps)

    def __setCurrFPS(self, fps: int):
        self.currFps = fps
        self.currFpsLabel.setText(babelfish.ui_curr_fps(fps))

    def __setFps(self, value):
        if value == self.currFps:
            qfw.InfoBar.success(
                title=babelfish.ui_setting_success(),
                content=babelfish.ui_fps_is_already(value),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                duration=2000,
                position=qfw.InfoBarPosition.TOP_RIGHT,
                parent=self,
            )
        else:
            self.setFpsThread = SetFpsThread(value, self)
            self.setFpsThread.successSignal.connect(self.__setSuccessSlot)
            self.setFpsThread.failureSignal.connect(self.__setFailureSlot)
            self.settingButton.setDisabled(True)
            self.resetButton.setDisabled(True)
            self.setFpsThread.start()

    def __setFpsSlot(self):
        targetFps = self.spinBox.value()
        self.__setFps(targetFps)

    def __resetFpsSlot(self):
        targetFps = default_fps
        self.__setFps(targetFps)

    def __setSuccessSlot(self, msg: str):
        self.__setCurrFPS(self.setFpsThread.value)
        self.settingButton.setEnabled(True)
        self.resetButton.setEnabled(True)
        self.setFpsThread = None

        qfw.InfoBar.success(
            title=babelfish.ui_setting_success(),
            content=msg,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=3000,
            position=qfw.InfoBarPosition.TOP_RIGHT,
            parent=self,
        )

    def __setFailureSlot(self, msg: str):
        self.settingButton.setEnabled(True)
        self.resetButton.setEnabled(True)
        self.setFpsThread = None

        qfw.InfoBar.error(
            title=babelfish.ui_setting_failure(),
            content=msg,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=-1,
            position=qfw.InfoBarPosition.TOP_RIGHT,
            parent=self,
        )
