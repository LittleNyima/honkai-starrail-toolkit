import traceback

from starrail import __version__, digital_version
from starrail.gui.common.config import qcfg
from starrail.gui.widgets.dialog import CheckUpdateDialog
from starrail.utils import babelfish
from starrail.utils.auto_update import check_update


def checkUpdate(parent):
    if qcfg.get(qcfg.check_update):
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
        except Exception:
            traceback.print_exc()
            dialog = CheckUpdateDialog(
                title=babelfish.ui_ooops(),
                content=babelfish.ui_check_update_fail(),
                parent=parent,
                dist=None,
            )
            dialog.show()
            dialog.raise_()
