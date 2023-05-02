import copy
import json
import os

from easydict import EasyDict

userroot = os.path.abspath(os.path.expanduser('~'))

configuration = EasyDict(
    cache_dir=os.path.join(userroot, '.starrail'),
    config_path=os.path.join(userroot, '.starrail', 'config.json'),
    check_update=True,
)


def export_config(cfg, skip_keys=[]):
    config_path = cfg.config_path
    cfg = copy.deepcopy(cfg)
    for key in skip_keys:
        if key in cfg:
            cfg.pop(key)
    with open(config_path, 'w', encoding='utf-8') as fcfg:
        json.dump(cfg, fcfg, indent=2, ensure_ascii=False)


def init_config():

    os.makedirs(configuration.cache_dir, exist_ok=True)

    if os.path.isfile(configuration.config_path):
        with open(configuration.config_path, encoding='utf-8') as fcfg:
            custom_config = json.load(fcfg)

        configuration.update(custom_config)
    else:
        export_config(
            configuration,
            skip_keys=['cache_dir', 'config_path'],
        )
