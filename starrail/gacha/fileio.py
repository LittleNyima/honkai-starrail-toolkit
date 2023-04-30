import json

import pandas as pd

from starrail.gacha.database import DatabaseFactory
from starrail.gacha.parse import GachaDataManager
from starrail.gacha.type import GachaType
from starrail.utils import loggings

logger = loggings.get_logger(__file__)


def export_as_sql(manager: GachaDataManager, output_path: str) -> None:
    logger.info(f'Exporting data to cache {output_path}')
    with DatabaseFactory.get_database(output_path) as db:
        for gacha_type in GachaType:
            should_insert = []
            for entry in manager.gacha[gacha_type.value]:
                if 'existing' in entry and not entry['existing']:
                    should_insert.append(entry)
            logger.info(
                f'Exporting {gacha_type.name}, '
                f'totally {len(should_insert)} new items',
            )
            rev_insert = reversed(should_insert)
            for entry in rev_insert:
                db.add_entry(gacha_type.name, entry)


def export_as_json(manager: GachaDataManager, output_path: str) -> None:
    data_dict = dict()
    for gacha_type in GachaType:
        data_dict[gacha_type.name] = manager.gacha[gacha_type.value].tolist()
    with open(output_path, 'w', encoding='utf-8') as fout:
        json.dump(data_dict, fout, indent=2, ensure_ascii=False)


def export_as_xlsx(manager: GachaDataManager, output_path: str) -> None:
    with pd.ExcelWriter(output_path) as writer:
        for gacha_type in GachaType:
            df = pd.json_normalize(manager.gacha[gacha_type.value].tolist())
            df.to_excel(writer, sheet_name=gacha_type.name)


def export_as_csv(manager: GachaDataManager, output_path: str) -> None:
    data_list = []
    for gacha_type in GachaType:
        data_list.extend(manager.gacha[gacha_type.value].tolist())
    df = pd.json_normalize(data_list)
    df.to_csv(output_path, encoding='utf-8')


def export_as_html(manager: GachaDataManager, output_path: str) -> None:
    raise NotImplementedError
