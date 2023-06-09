import traceback

from PySide6.QtCore import QThread, Signal

from starrail.utils import babelfish, loggings

logger = loggings.get_logger(__file__)


class StatefulThread(QThread):

    successSignal = Signal(str)
    failureSignal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def run(self):
        try:
            msg = self.work()
            self.successSignal.emit(msg)
        except Exception:
            logger.error(traceback.format_exc())
            msg = f'{babelfish.ui_traceback()}:\n{traceback.format_exc()}'
            self.failureSignal.emit(msg)

    def work(self):
        raise NotImplementedError
