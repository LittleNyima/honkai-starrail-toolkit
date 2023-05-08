import os

from starrail.config import configuration as cfg


def get_current_uid():
    if cfg.uid:
        return cfg.uid
    if os.path.isdir(cfg.db_dir):
        dbs = os.listdir(cfg.db_dir)
        dbs = [db.split('.')[0] for db in dbs if db.endswith('.sqlite3')]
        if dbs:
            return sorted(dbs)[0]
    return ''
