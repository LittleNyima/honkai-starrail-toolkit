import os

from starrail.config import configuration as cfg
from starrail.gacha.fileio import GachaDatabase
from starrail.gacha.type import GachaType


class GachaDataList:
    def __init__(self, name, iterable=[], hash_key='id'):
        self.name = name
        self.data = []
        self.hash = set()
        self.hash_key = hash_key
        self.extend(iterable)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def append(self, item):
        if item[self.hash_key] not in self.hash:
            self.data.append(item)
            self.hash.add(item[self.hash_key])
            return True
        return False

    def extend(self, iterable):
        return [self.append(item) for item in iterable]

    def sort(self):
        self.data.sort(key=lambda x: x[self.hash_key])


class GachaDataManager:

    def __init__(self, uid):
        self.gacha = init_empty_gacha_record()
        self.load_cache(uid)

    def load_cache(self, uid: str):
        cache_dir = cfg.cache_dir
        cache_path = os.path.join(cache_dir, f'{uid}.sqlite3')
        if os.path.isfile(cache_path):
            self.gacha = parse_cache_from_sql(cache_path)


def parse_cache_from_sql(cache_path):
    db = GachaDatabase(cache_path)
    cache = dict()
    for gacha_type in GachaType:
        entries = db.get_entries(gacha_type.name)
        data_list = GachaDataList(gacha_type.name, entries)
        cache[gacha_type.value] = data_list
    return cache


def init_empty_gacha_record():
    return {gt.value: GachaDataList(gt.name) for gt in GachaType}
