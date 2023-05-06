import copy
import os
from typing import Dict

from prettytable import PrettyTable

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

    @property
    def stats(self):
        data = []
        for rank_type in ['5', '4', '3']:
            data.append(self.substats(rank_type))
        return data

    def substats(self, rank_type):
        count = sum([
            1 if item['rank_type'] ==
            rank_type else 0 for item in self.data
        ])
        total_items = len(self.data)
        if not total_items or not count:
            return dict(
                rank_type=rank_type,
                count='0',
                basic_prob='',
                compr_prob='',
                since_last='',
                attempts=[],
                average='',
            )
        if rank_type == '3':
            return dict(
                rank_type=rank_type,
                count=f'{count}',
                basic_prob=f'{count / total_items:.2%}',
                compr_prob='',
                since_last='',
                attempts=[],
                average='',
            )
        attempts = []
        current_stats, current_attempts = None, 0
        for item in self.data + [dict(rank_type=rank_type, name='dummy')]:
            if item['rank_type'] == rank_type:
                attempts.append((current_stats, current_attempts))
                current_stats, current_attempts = item['name'], 0
            current_attempts += 1
        since_last = attempts[0][1]
        attempts = [f'{name}@{times}' for (name, times) in attempts]
        return dict(
            rank_type=rank_type,
            count=f'{count}',
            basic_prob=f'{count / total_items:.2%}',
            compr_prob=f'{count / (total_items - since_last):.2%}',
            since_last=f'{since_last}',
            attempts=attempts[1:],
            average=f'{(total_items - since_last) / count:.2f}',
        )


class GachaDataManager:

    def __init__(self, uid):
        self.uid = uid
        self.gacha = self.load_cache(uid)

    def load_cache(self, uid: str):
        db_dir = cfg.db_dir
        self.cache_path = os.path.join(db_dir, f'{uid}.sqlite3')
        if os.path.isfile(self.cache_path):
            return parse_cache_from_sql(self.cache_path)
        return init_empty_gacha_record()

    def log_stats(self):
        # a simple version
        fileds = ['Type', 'Count', 'Basic Prob.', ' True Prob.', 'Since Last']
        stats_string = f'*** Gacha stats for user uid = {self.uid}:\n'
        for gacha_type in GachaType:
            stats_string += f'  * {gacha_type.name}\n'
            stats = self.gacha[gacha_type.value].stats
            table = PrettyTable(field_names=fileds)
            for item in stats:
                table.add_row([
                    item['rank_type'], item['count'],
                    item['basic_prob'], item['compr_prob'],
                    item['since_last'],
                ])
            pretty = table.get_string()
            stats_string += f'{pretty}\n'
            if stats[0]['attempts']:
                attempt_string = ' '.join(stats[0]['attempts'])
                average = stats[0]['average']
                stats_string += ' History of 5-star gacha attempts: '
                stats_string += attempt_string
                stats_string += f'\n Average gacha per 5-star: {average}\n'
            stats_string += '\n'

        logger.info(stats_string)

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
