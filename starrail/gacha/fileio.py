import json
import time

import pandas as pd

import starrail
import starrail.utils.babelfish as babelfish
from starrail.gacha.factory import DatabaseFactory
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


def export_as_md(manager: GachaDataManager, output_path: str) -> None:
    md = f'# {babelfish.gacha_report()}\n\n'
    for gacha_type in GachaType:
        md += f'## {babelfish.translate(gacha_type.name)}\n\n'
        md += babelfish.markdown_thead()
        stats = manager.gacha[gacha_type.value].stats
        for item in stats:
            rtype = item['rank_type']
            count = item['count']
            basic = item['basic_prob']
            compr = item['compr_prob']
            since_last = item['since_last']
            md += f'|{rtype}|{count}|{basic}|{compr}|{since_last}|\n'
        md += '\n'
        if stats[0]['attempts']:
            attempt_string = ' '.join(stats[0]['attempts'])
            average = stats[0]['average']
            md += f'{babelfish.history_of_5_stars()}: '
            md += f'**{attempt_string}**\n\n'
            md += f'{babelfish.average_gacha_per_5_star()}: **{average}**\n\n'
    with open(output_path, 'w', encoding='utf-8') as fout:
        fout.write(md)


def export_as_html(manager: GachaDataManager, output_path: str) -> None:
    title = f'{babelfish.gacha_title(manager.uid)}'
    content = f'<h1>{babelfish.gacha_report()}</h1>\n'
    for gacha_type in GachaType:
        content += f'<h2>{babelfish.translate(gacha_type.name)}</h2>\n'
        thead = babelfish.html_thead()
        table = f'<table><thead><tr>{thead}</tr></thead><tbody>\n'
        stats = manager.gacha[gacha_type.value].stats
        for item in stats:
            rtype = item['rank_type']
            count = item['count']
            basic = item['basic_prob']
            compr = item['compr_prob']
            since_last = item['since_last']
            table += (
                f'<tr><td>{rtype}</td><td>{count}</td><td>{basic}</td>'
                f'<td>{compr}</td><td>{since_last}</td></tr>\n'
            )
        table += '</tbody></table>\n'
        content += table
        if stats[0]['attempts']:
            attempt_string = ' '.join(stats[0]['attempts'])
            average = stats[0]['average']
            content += f'<p>{babelfish.history_of_5_stars()}: '
            content += f'<b>{attempt_string}</b></p>\n'
            content += f'<p>{babelfish.average_gacha_per_5_star()}: '
            content += f'<b>{average}</b></p>\n'
    style = (
        '<style type="text/css">'
        r'html {font-family: sans-serif;} '
        r'body {margin: 10px;} '
        r'table {border-collapse: collapse; border-spacing: 0;'
        r'       empty-cells: show; border: 1px solid #cbcbcb;} '
        r'td, th {padding: 0; border-left: 1px solid #cbcbcb;'
        r'        border-width: 0 0 0 1px; font-size: inherit;'
        r'        margin: 0; overflow: visible; padding: .5em 1em;} '
        r'thead {background-color: #e0e0e0; color: #000;'
        r'       text-align: left; vertical-align: bottom; }'
        r'tr:nth-child(odd) td {background-color: transparent;} '
        r'tr:nth-child(even) td {background-color: #f2f2f2;} '
        '</style>'
    )
    html = (
        f'<html lang="zh"><head><title>{title}</title><meta charset="UTF-8">'
        f'{style}</head><body>{content}</body></html>'
    )
    with open(output_path, 'w', encoding='utf-8') as fout:
        fout.write(html)


def export_as_srgf(manager: GachaDataManager, output_path: str) -> None:
    gacha_list = []
    for gacha_type in GachaType:
        gacha_list.extend(manager.gacha[gacha_type.value].tolist())
    gacha_list.sort(key=lambda x: x['id'])
    uid = gacha_list[-1]['uid'] if gacha_list else manager.uid
    lang = gacha_list[-1]['lang'] if gacha_list else 'zh-cn'
    timezone = gacha_list[-1]['region_time_zone'] if gacha_list else '8'
    timezone = int(timezone)
    timestamp = int(time.time())
    data = dict(
        info=dict(
            uid=uid,
            lang=lang,
            region_time_zone=timezone,
            export_timestamp=timestamp,
            export_app='StarRailToolkit',
            export_app_version=starrail.__version__,
            srgf_version='v1.0',
        ),
        list=[
            dict(
                gacha_id=item['gacha_id'],
                gacha_type=item['gacha_type'],
                item_id=item['item_id'],
                count=item['count'],
                time=item['time'],
                name=item['name'],
                item_type=item['item_type'],
                rank_type=item['rank_type'],
                id=item['id'],
            ) for item in gacha_list
        ],
    )
    with open(output_path, 'w', encoding='utf-8') as fout:
        json.dump(data, fout, indent=2, ensure_ascii=False)
