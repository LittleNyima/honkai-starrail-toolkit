import sys

from starrail.config import configuration as cfg
from starrail.entry.setup import setup
from starrail.utils import loggings

logger = loggings.get_logger(__file__)

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication

    from starrail.gui.application import StarRailToolkit
except ImportError as e:
    logger.critical(
        'Graphic mode is defaultly not enabled. If you want to run the GUI, '
        'please download the executables or launch from the source code. '
        'See: https://github.com/LittleNyima/honkai-starrail-toolkit for '
        'further information.',
    )
    raise e


def gui_entry():
    setup(log_level=cfg.log_level, locale=cfg.locale)

    AA = Qt.ApplicationAttribute
    app = QApplication(sys.argv)
    app.setAttribute(AA.AA_DontCreateNativeWidgetSiblings)

    window = StarRailToolkit()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    gui_entry()
