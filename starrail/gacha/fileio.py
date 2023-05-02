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


def export_as_md(manager: GachaDataManager, output_path: str) -> None:
    md = '# Gacha Report\n\n'
    for gacha_type in GachaType:
        md += f'## {gacha_type.name}\n\n'
        md += (
            '| Type | Count | Basic Prob. | True Prob. | Since Last |\n'
            '| ---- | ----- | ----------- | ---------- | ---------- |\n'
        )
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
            md += 'History of 5-star gacha attempts: '
            md += f'**{attempt_string}**'
            md += '\n\n'
            md += f'Average gacha per 5-star: **{average}**\n\n'
    with open(output_path, 'w', encoding='utf-8') as fout:
        fout.write(md)


def export_as_html(manager: GachaDataManager, output_path: str) -> None:
    title = f'Gacha Report for Honkai: Star Rail Player {manager.uid}'
    content = '<h1>Gacha Report</h1>\n'
    for gacha_type in GachaType:
        content += f'<h2>{gacha_type.name}</h2>\n'
        table = (
            '<table><thead><tr><th>Type</th><th>Count</th>'
            '<th>Basic Prob.</th><th>True Prob.</th><th>Since Last</th>'
            '</tr></thead><tbody>\n'
        )
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
            content += '<p>History of 5-star gacha attempts: '
            content += f'<b>{attempt_string}</b></p>\n'
            content += f'<p>Average gacha per 5-star: <b>{average}</b></p>\n'
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
