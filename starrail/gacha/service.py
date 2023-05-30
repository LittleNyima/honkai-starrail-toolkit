import json
import os
import time
import traceback
from collections import defaultdict

import starrail.gacha.fileio as fileio
from starrail.gacha.autodet import detect_api_url
from starrail.gacha.fetch import fetch_json
from starrail.gacha.parse import GachaDataManager
from starrail.gacha.type import GachaType
from starrail.gacha.url import get_api_url, get_url_template
from starrail.utils import babelfish, loggings
from starrail.utils.accounts import account_record

logger = loggings.get_logger(__file__)


def integers():
    r = 1
    while True:
        yield r
        r += 1


def check_response(payload, code):
    # returns: is_valid, should_stop, massage
    resp = json.dumps(payload, ensure_ascii=False)
    if payload is None:  # check payload
        return False, True, f'Payload is None, response: {resp}'
    elif not 200 <= code < 300:  # check request
        return False, True, f'Request fail, code: {code}, response: {resp}'
    elif 'data' not in payload:  # check data
        return False, True, f'data is not in payload, response: {resp}'
    elif not payload['data']:  # check data empty or null
        return False, True, f'data is empty or None, response: {resp}'
    elif 'list' not in payload['data']:  # check field
        return False, True, f'data.list is missing, response: {resp}'
    elif not payload['data']['list']:  # check data list
        return True, True, 'valid but reaching the end of list'
    return True, False, 'ok'


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
            str(page), '20',
        )
        logger.debug(f'Requesting {api_url}')
        response, code = fetch_json(api_url)
        time.sleep(request_interval)
        _, should_stop, msg = check_response(response, code)
        logger.info(f'check_response: {msg}')
        if should_stop:
            break
        data_list = response['data']['list']
        region = response['data']['region']
        timezone = response['data']['region_time_zone']
        metainfo = dict(region=region, region_time_zone=timezone)
        for data_item in data_list:
            data_item.update(metainfo)
        r.extend(data_list)
        end_id = data_list[-1]['id']
    return r


def deduce_uid(record_cache):
    for gacha_type in GachaType:
        records = record_cache[gacha_type.value]
        if records:
            return records[0]['uid']
    return ''


def export_gacha_from_api(api_url, export, request_interval):
    if not api_url:
        api_url = detect_api_url()
    response, code = fetch_json(api_url)
    valid, _, msg = check_response(response, code)
    logger.info(f'check_response (api): {msg}')
    if not valid:
        logger.fatal('Error while checking response from api URL, exitting')
        raise ValueError('Invalid or expired api, please check your input')

    api_template = get_url_template(api_url)
    record_cache = dict()

    for gacha_type in GachaType:
        records = export_gacha_type(
            api_template,
            gacha_type,
            request_interval,
        )
        record_cache[gacha_type.value] = records
        logger.info(f'Finish downloading records of {gacha_type.name}')

    uid = deduce_uid(record_cache)
    if not uid:
        logger.fatal(
            'Cannot deduce uid from records, there may be no gacha '
            'record. Please check your account and try again.',
        )
        raise ValueError('Cannot deduce uid from records')
    manager = GachaDataManager(uid)
    logger.info(f'Successfully connected to cache of uid {uid}')
    manager.log_stats()

    for gacha_type in GachaType:
        manager.add_records(gacha_type.value, record_cache[gacha_type.value])
        manager.gacha[gacha_type.value].sort()

    fileio.export_as_sql(manager, manager.cache_path)

    account_record.update_timestamp(uid)
    manager.log_stats()

    export_hooks = dict(
        csv=fileio.export_as_csv,
        html=fileio.export_as_html,
        json=fileio.export_as_json,
        md=fileio.export_as_md,
        srgf=fileio.export_as_srgf,
        xlsx=fileio.export_as_xlsx,
    )
    if 'all' in export:
        export = ['csv', 'html', 'json', 'md', 'srgf', 'xlsx']

    timestamp = time.strftime('%Y%m%d%H%M%S')

    for format in export:
        logger.info(f'Exporting gacha data as {format} format')
        output_dir = os.getcwd()
        filename = f'HKSR-export-{uid}-{timestamp}.{format}'
        if format == 'srgf':
            filename += '.json'
        path = os.path.join(output_dir, filename)
        export_hooks[format](manager, path)
        logger.info(f'Gacha data in {format} format is saved to {path}')


def import_srgf_data(filename):
    if not filename:
        logger.info('Skipping import srgf data')
        return
    try:
        with open(filename, encoding='utf-8') as f:
            data = json.load(f)
        info = data['info']
        uid = info['uid']
        update_info = dict(
            uid=info['uid'],
            lang=info['lang'],
            region='',  # unused
            region_time_zone=str(info['region_time_zone']),
        )
        record_cache = defaultdict(list)
        for item in data['list']:
            item.update(update_info)
            record_cache[int(item['gacha_type'])].append(item)

        manager = GachaDataManager(uid=uid)
        logger.info(f'Successfully connected to cache of uid {uid}')
        manager.log_stats()

        for k, v in record_cache.items():
            manager.add_records(k, v)
            manager.gacha[k].sort()

        fileio.export_as_sql(manager, manager.cache_path)

        timestamp = info['export_timestamp']
        timestruct = time.localtime(timestamp)
        timestr = time.strftime(babelfish.constants.TIME_FMT, timestruct)
        account_record.update_timestamp(uid, timestr)

        logger.info(f'Successfully load gacha data from {filename}')
    except Exception:
        logger.error('Import gacha data failed. Traceback:')
        logger.error(traceback.format_exc())
