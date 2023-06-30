import json
import os
import time
from typing import Dict

import easydict

from starrail.config import configuration as cfg
from starrail.utils import babelfish, security


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
        self.secrets = dict()
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

    def set_user_property(self, uid: str, key: str, value):
        self.accounts[uid][key] = value
        self.flush()

    def set_secrets(self, uid: str, secrets: Dict[str, str]):
        self.secrets[uid] = secrets
        secret_str = json.dumps(secrets)
        iv, encrypted = security.AES192.encrypt(
            secret_str, security.token_aes128_key16b,
        )
        self.accounts[uid]['iv'] = security.Base64.encode(iv)
        self.flush()
        storage_path = os.path.join(cfg.user_info_dir, uid)
        with open(storage_path, 'wb') as fout:
            fout.write(encrypted)

    def load_secrets(self, uid: str):
        storage_path = os.path.join(cfg.user_info_dir, uid)
        with open(storage_path, 'rb') as fin:
            encrypted = fin.read()
        iv = security.Base64.decode(self.accounts[uid]['iv'])
        secret_str = security.AES192.decrypt(
            encrypted, security.token_aes128_key16b, iv,
        )
        self.secrets[uid] = json.loads(secret_str)

    def get_secret(self, uid: str, key: str):
        if uid not in self.secrets:
            self.load_secrets(uid)
        return self.secrets[uid][key]


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
