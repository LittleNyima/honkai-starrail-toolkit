import json
import os
import time

import easydict

from starrail.config import configuration as cfg
from starrail.utils import babelfish


def todict(d, keys):
    """
    Filters a dictionary by keeping only the specified keys and returns a new
    dictionary with those key-value pairs.

    Args:
        d (dict): The input dictionary to filter.
        keys (iterable): An iterable of keys that should be kept in the output
            dictionary.

    Returns:
        dict: A new dictionary containing only the specified key-value pairs
            from the input dictionary.
    """

    return {k: d[k] for k in d if k in keys}


class AccountRecord:

    # callbacks
    latest_uid_changed = None
    accounts_changed = None

    def __init__(self, path):
        self._path = path
        cache = self.safe_load()
        self.meta = cache['meta']
        self.accounts = cache['accounts']
        self.init_keys()

    def init_keys(self, keys=('last_update', 'iv')):
        keys_set = set(keys)
        for uid in self.accounts:
            user_keys_set = set(self.accounts[uid])
            del_keys_set = user_keys_set - keys_set
            add_keys_set = keys_set - user_keys_set
            for del_key in del_keys_set:
                del self.accounts[uid][del_key]
            for add_key in add_keys_set:
                self.accounts[uid][add_key] = ''
        self.flush()

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
                iv='',
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

    def get_user_properties(self, uid: str):
        uid = str(uid)
        return easydict.EasyDict(self.accounts[uid])


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
