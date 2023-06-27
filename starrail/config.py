import json
import os

from easydict import EasyDict

userroot = os.path.abspath(os.path.expanduser('~'))
srroot = os.path.join(userroot, '.starrail')


class Configuration(EasyDict):

    def __init__(self, d=None, **kwargs):
        self.no_flush = True
        self.skip_keys = set()
        self.user_keys = set(kwargs.keys())
        super().__init__(d, **kwargs)
        self.no_flush = False

    def set_skip_keys(self, *args: str):
        self.skip_keys |= set(args)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if (
            not self.no_flush
            and name in self.user_keys
            and name not in self.skip_keys
        ):
            self.flush()

    def flush(self):
        if not self.no_flush:
            cfg = {
                k: self[k]
                for k in self.user_keys if k not in self.skip_keys
            }
            with open(self.config_path, 'w', encoding='utf-8') as fcfg:
                json.dump(cfg, fcfg, indent=2)


configuration = Configuration(
    cache_dir=srroot,
    db_dir=os.path.join(srroot, 'database'),
    config_path=os.path.join(srroot, 'config.json'),
    account_record_path=os.path.join(srroot, 'accounts.json'),
    res_cache_dir=os.path.join(srroot, 'cache'),
    user_info_dir=os.path.join(srroot, 'userinfo'),
    check_update=True,
    locale='zhs',
    log_level='DEBUG',
)
configuration.set_skip_keys(
    'skip_keys', 'no_flush',
    'cache_dir', 'config_path', 'db_dir', 'account_record_path',
    'res_cache_dir', 'user_info_dir',
)


def init_config():

    os.makedirs(configuration.cache_dir, exist_ok=True)
    os.makedirs(configuration.db_dir, exist_ok=True)
    os.makedirs(configuration.res_cache_dir, exist_ok=True)
    os.makedirs(configuration.user_info_dir, exist_ok=True)

    if os.path.isfile(configuration.config_path):
        with open(configuration.config_path, encoding='utf-8') as fcfg:
            custom_config = json.load(fcfg)

        configuration.update(custom_config)
    else:
        configuration.flush()
