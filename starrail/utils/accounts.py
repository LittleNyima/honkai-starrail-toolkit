import json
import os
import time

from starrail.config import configuration as cfg
from starrail.utils import babelfish


def todict(d, keys):
    return {k: d[k] for k in d if k in keys}


class AccountRecord:

    latest_uid_changed = None
    accounts_changed = None

    def __init__(self, path):
        self._path = path
        cache = self.safe_load()
        self.meta = cache['meta']
        self.accounts = cache['accounts']

    def safe_load(self):
        try:
            with open(self._path, encoding='utf-8') as f:
                cache = json.load(f)
            return cache
        except Exception:
            return dict(
                meta=dict(latest=''),
                accounts=dict(),
            )

    def flush(self):
        dirname = os.path.dirname(self._path)
        os.makedirs(dirname, exist_ok=True)
        with open(self._path, 'w', encoding='utf-8') as f:
            json.dump(
                dict(meta=self.meta, accounts=self.accounts), f,
                ensure_ascii=False, indent=2,
            )

    def add_account(self, uid: str):
        uid = str(uid)
        if uid not in self.accounts:
            self.accounts[uid] = dict(
                last_update='',
                pid='',
                cookie='',
            )
            if self.accounts_changed is not None:
                self.accounts_changed()

    def update_timestamp(self, uid, timestamp=None):
        uid = str(uid)
        self.latest_uid = uid
        if not timestamp:
            timestamp = time.strftime(babelfish.constants.TIME_FMT)
        if uid not in self.accounts:
            self.add_account(uid)
        self.accounts[uid]['last_update'] = timestamp
        self.flush()

    @property
    def latest_uid(self):
        return self.meta['latest']

    @latest_uid.setter
    def latest_uid(self, value):
        if self.meta['latest'] != value:
            self.meta['latest'] = value
            if self.latest_uid_changed is not None:
                self.latest_uid_changed(value)


account_record = AccountRecord(cfg.account_record_path)


def get_latest_uid():
    if account_record.latest_uid:
        return account_record.latest_uid
    if os.path.isdir(cfg.db_dir):
        caches = os.listdir(cfg.db_dir)
        caches = [
            cache.split('.')[0]
            for cache in caches if cache.endswith('.sqlite3')
        ]
        if caches:
            return sorted(caches)[0]
    return ''
