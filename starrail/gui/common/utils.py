import traceback

import qfluentwidgets as qfw
from PySide6.QtCore import Qt

from starrail import __version__, digital_version
from starrail.gui.widgets.dialog import CheckUpdateDialog
from starrail.utils import babelfish
from starrail.utils.auto_update import check_update


def checkUpdate(parent, show_success=False, show_failure=True):
    try:
        latest = check_update()
        current = digital_version(__version__)
        if current < digital_version(latest.version):
            dialog = CheckUpdateDialog(
                title=babelfish.ui_update_available(),
                content=babelfish.ui_update_desc(latest.changelog),
                parent=parent,
                dist=latest.dist,
            )
            dialog.show()
            dialog.raise_()
        elif show_success:
            qfw.InfoBar.success(
                title=babelfish.ui_check_update_success(),
                content=babelfish.ui_is_latest_version(),
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                duration=3000,
                position=qfw.InfoBarPosition.TOP_RIGHT,
                parent=parent,
            )
    except Exception:
        traceback.print_exc()
        if show_failure:
            dialog = CheckUpdateDialog(
                title=babelfish.ui_ooops(),
                content=babelfish.ui_check_update_fail(),
                parent=parent,
                dist=None,
            )
            dialog.show()
            dialog.raise_()
