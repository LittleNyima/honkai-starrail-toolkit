import os
import time
from datetime import datetime

import starrail.gacha.fileio as fileio
from starrail.gacha.autodet import detect_api_url
from starrail.gacha.fetch import fetch_json
from starrail.gacha.parse import GachaDataManager
from starrail.gacha.type import GachaType
from starrail.gacha.url import get_api_url, get_url_template
from starrail.utils import loggings

logger = loggings.get_logger(__file__)


def integers():
    r = 1
    while True:
        yield r
        r += 1


def check_response(payload, code):
    if payload is None or not 200 <= code < 300:
        logger.info(f'Whether payload is None: {payload is None}')
        logger.info(f'Status code: {code}')
        return False
    if 'data' not in payload or 'list' not in payload['data']:
        logger.info(f'Whether payload contains `data`: {"data" in payload}')
        logger.info(
            f'Whether payload data contains `list`:'
            f'{"list" in payload["data"]}',
        )
        return False
    if not payload['data']['list']:
        logger.info(
            f'Length of payload.data.list: '
            f'{len(payload["data"]["list"])}',
        )
        return False
    return True


def export_gacha_type(
    api_template: str,
    gacha_type: GachaType,
    request_interval: float,
):
    r = []
    end_id = '0'
    for page in integers():
        logger.info(f'Downloading page {page} of type {gacha_type.name}')
        api_url = get_api_url(
            api_template, end_id, str(gacha_type.value),
            str(page), '5',
        )
        logger.debug(f'Requesting {api_url}')
        response, code = fetch_json(api_url)
        time.sleep(request_interval)
        if not check_response(response, code):
            break
        data_list = response['data']['list']
        r.extend(data_list)
        end_id = data_list[-1]['id']
    return r


def export_gacha_from_api(api_url, export, request_interval):
    if not api_url:
        api_url = detect_api_url()
    response, code = fetch_json(api_url)
    valid = check_response(response, code)
    if not valid:
        logger.fatal('Error while checking response from api URL, exitting')
        raise ValueError('Invalid or expired api, please check your input')

    api_template = get_url_template(api_url)

    uid = response['data']['list'][0]['uid']
    manager = GachaDataManager(uid)
    logger.info(f'Successfully connected to cache of uid {uid}')
    manager.log_stats()

    for gacha_type in GachaType:
        records = export_gacha_type(
            api_template,
            gacha_type,
            request_interval,
        )
        manager.add_records(gacha_type.value, records)
        manager.gacha[gacha_type.value].sort()
        logger.info(f'Finish downloading records of {gacha_type.name}')

    fileio.export_as_sql(manager, manager.cache_path)

    manager.log_stats()

    export_hooks = dict(
        csv=fileio.export_as_csv,
        html=fileio.export_as_html,
        json=fileio.export_as_json,
        md=fileio.export_as_md,
        xlsx=fileio.export_as_xlsx,
    )
    if 'all' in export:
        export = ['csv', 'html', 'json', 'md', 'xlsx']

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    for format in export:
        logger.info(f'Exporting gacha data as {format} format')
        output_dir = os.getcwd()
        filename = f'HKSR-export-{uid}-{timestamp}.{format}'
        path = os.path.join(output_dir, filename)
        export_hooks[format](manager, path)
        logger.info(f'Gacha data in {format} format is saved to {path}')
