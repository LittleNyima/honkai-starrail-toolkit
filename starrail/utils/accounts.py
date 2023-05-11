import json
import os
from datetime import datetime

from starrail.config import configuration as cfg
from starrail.utils import babelfish


def todict(d, keys):
    return {k: d[k] for k in d if k in keys}


class AccountRecord:

    def __init__(self, path):
        self._path = path
        cache = self.safe_load()
        self.meta = cache['meta']
        self.accounts = cache['accounts']

    def safe_load(self):
        try:
            with open(self.path, encoding='utf-8') as f:
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

    def update_timestamp(self, uid):
        timestamp = datetime.now().strftime(babelfish.constants.TIME_FMT)
        if uid in self.accounts:
            self.accounts[uid]['last_update'] = timestamp
        else:
            self.accounts[uid] = dict(last_update=timestamp)
        self.meta['latest'] = uid
        self.flush()

    def latest_uid(self):
        return self.meta['latest']


account_record = AccountRecord(cfg.account_record_path)
account_record.flush()


def get_latest_uid():
    if account_record.latest_uid():
        return account_record.latest_uid()
    if os.path.isdir(cfg.db_dir):
        caches = os.listdir(cfg.db_dir)
        caches = [
            cache.split('.')[0]
            for cache in caches if cache.endswith('.sqlite3')
        ]
        if caches:
            return sorted(caches)[0]
    return ''
