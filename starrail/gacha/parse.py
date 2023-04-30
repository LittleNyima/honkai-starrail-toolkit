import copy
import os
from typing import Dict

from starrail.config import configuration as cfg
from starrail.gacha.database import DatabaseFactory
from starrail.gacha.type import GachaType
from starrail.utils import loggings

logger = loggings.get_logger(__file__)


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
        self.data.sort(key=lambda x: -int(x[self.hash_key]))

    def tolist(self):
        return copy.deepcopy(self.data)


class GachaDataManager:

    def __init__(self, uid):
        self.uid = uid
        self.gacha = self.load_cache(uid)

    def load_cache(self, uid: str):
        cache_dir = cfg.cache_dir
        self.cache_path = os.path.join(cache_dir, f'{uid}.sqlite3')
        if os.path.isfile(self.cache_path):
            return parse_cache_from_sql(self.cache_path)
        return init_empty_gacha_record()

    def log_stats(self):
        # a simple version
        logger.info(f'Gacha stats for uid {self.uid}:')
        for gacha_type in GachaType:
            rec_length = len(self.gacha[gacha_type.value])
            logger.info(f'  {gacha_type.name} - {rec_length}')

    def add_records(self, gacha_id, records):
        r = self.gacha[gacha_id].extend(records)
        for success, record in zip(r, records):
            record['existing'] = not success


def parse_cache_from_sql(cache_path: str) -> Dict[int, GachaDataList]:
    cache = dict()
    with DatabaseFactory.get_database(cache_path) as db:
        for gacha_type in GachaType:
            entries = db.get_entries(gacha_type.name)
            data_list = GachaDataList(gacha_type.name, entries)
            cache[gacha_type.value] = data_list
    return cache


def init_empty_gacha_record() -> Dict[int, GachaDataList]:
    return {gt.value: GachaDataList(gt.name) for gt in GachaType}
