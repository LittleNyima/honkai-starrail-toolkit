import os
import traceback

from starrail import __version__, digital_version
from starrail.config import configuration as cfg
from starrail.gui.widgets.dialog import CheckUpdateDialog
from starrail.utils import babelfish
from starrail.utils.auto_update import check_update


def get_current_uid():
    if cfg.uid:
        return cfg.uid
    if os.path.isdir(cfg.db_dir):
        dbs = os.listdir(cfg.db_dir)
        dbs = [db.split('.')[0] for db in dbs if db.endswith('.sqlite3')]
        if dbs:
            return sorted(dbs)[0]
    return ''


def checkUpdate(parent):
    if cfg.check_update:
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
