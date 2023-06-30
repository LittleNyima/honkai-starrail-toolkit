import functools
import random
import time
import traceback
import uuid
from typing import Any, Callable, Dict, Hashable, Optional
from urllib.parse import parse_qs, urlparse

import requests

from starrail.mihoyo import api, dynamic_secret
from starrail.utils import loggings

logger = loggings.get_logger(__file__)


def enter(prefix: str = '[HoyolabClient]') -> Callable:
    """
    Given a prefix string, creates a decorator that logs the function name
    with the given prefix when the decorated function is called.

    Args:
        prefix (str, optional): A custom prefix to be displayed in the log
            message. Defaults to an empty string.

    Returns:
        Callable: A decorator that accepts a function and returns a wrapped
            function.

    Example:
        >>> @enter("My Prefix: ")
        ... def my_function():
        ...     pass
    """

    def log_func(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            infostr = f'{prefix} {func.__name__}' if prefix else func.__name__
            logger.info(infostr)
            return func(*args, **kwargs)
        return wrapper

    return log_func


def random_hexstring(length: int) -> str:
    """
    Generates a random hexadecimal string of the specified length
    Args:
        length (int): The desired length of the hexadecimal string.
    Returns:
        str: A random hexadecimal string of the specified length.
    """

    hexdigits = '0123456789abcdef'
    return ''.join(random.choice(hexdigits) for _ in range(length))


class ExpirableCache:

    def __init__(self, expires: float):
        self.expires = expires
        self.cache_data: Dict[Hashable, Dict[str, Any]] = dict()

    def set(self, key: Hashable, value: Any):
        curr_time = time.time()
        expire_time = curr_time + self.expires
        self.cache_data[key] = dict(
            expire_time=expire_time,
            data=value,
        )

    def get(self, key: Hashable) -> Any:
        if key in self.cache_data:
            curr_time = time.time()
            expire_time = self.cache_data[key]['expire_time']
            if curr_time < expire_time:
                return self.cache_data[key]['data']
        return None


class HoyolabClient:

    xrpc_version = '2.50.1'

    user_agent = 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) miHoYoBBS/2.50.1'

    device_fp_cache = ExpirableCache(expires=300.0)

    def request_json(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        timeout=None,
    ):
        logger.debug(f'requesting json: {url}')
        response = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            timeout=timeout,
        )
        payload = response.json()
        logger.debug(payload)
        return payload

    def xrpc2_headers(
        self,
        device_id: str,
        extra: Dict[str, str] = {},
        **kwargs: str,
    ):
        headers = {
            'Accept': 'application/json',
            'User-Agent': HoyolabClient.user_agent,
            'x-rpc-aigis': '',
            'x-rpc-app_id': 'bll8iq97cem8',
            'x-rpc-app_version': HoyolabClient.xrpc_version,
            'x-rpc-client_type': '2',
            'x-rpc-device_id': device_id,
            'x-rpc-game_biz': 'bbs_cn',
            'x-rpc-sdk_version': '1.3.1.2',
        }
        headers.update(extra, **kwargs)
        return headers

    def xrpc5_headers(
        self,
        device_id: str,
        extra: Dict[str, str] = {},
        **kwargs: str,
    ):
        headers = {
            'Accept': 'application/json',
            'User-Agent': HoyolabClient.user_agent,
            'x-rpc-app_version': HoyolabClient.xrpc_version,
            'x-rpc-client_type': '5',
            'x-rpc-device_id': device_id,
        }
        headers.update(extra, **kwargs)
        return headers

    def xrpc11_headers(
        self,
        device_id: str,
        extra: Dict[str, str] = {},
        **kwargs: str,
    ):
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': HoyolabClient.user_agent,
            'x-rpc-aigis': '',
            'x-rpc-app_id': 'bll8iq97cem8',
            'x-rpc-app_version': HoyolabClient.xrpc_version,
            'x-rpc-client_type': '2',
            'x-rpc-device_fp': self.get_cached_device_fp(device_id),
            'x-rpc-device_id': device_id,
            'x-rpc-device_model': 'Chrome 108.0.0.0',
            'x-rpc-device_name': 'Windows 11 64-bit',
            'x-rpc-game_biz': 'bbs_cn',
            'x-rpc-sys_version': '11',
        }
        headers.update(extra, **kwargs)
        return headers

    def hoyolab_headers(
        self, ds: str, origin: str, referer: str, cookie: str,
        client_type: str, device_id: str, page: str,
        extra: Dict[str, str] = {},
        **kwargs: str,
    ):
        headers = {
            'DS': ds,
            'Origin': origin,
            'Referer': referer,
            'User-Agent': HoyolabClient.user_agent,
            'cookie': cookie,
            'x-rpc-app_version': HoyolabClient.xrpc_version,
            'x-rpc-client_type': client_type,
            'x-rpc-device_fp': self.get_cached_device_fp(device_id),
            'x-rpc-device_id': device_id,
            'x-rpc-device_model': 'Chrome 108.0.0.0',
            'x-rpc-device_name': 'Windows 11 64-bit',
            'x-rpc-page': page,
            'x-rpc-sys_version': '12',
        }
        headers.update(extra, **kwargs)
        return headers

    def hoyolab_xrpc2_headers(
        self, ds: str, cookie: str, device_id: str, page: str,
        extra: Dict[str, str] = {},
        **kwargs: str,
    ):
        return self.hoyolab_headers(
            ds=ds, origin='https://app.mihoyo.com/',
            referer='https://app.mihoyo.com/', cookie=cookie, client_type='2',
            device_id=device_id, page=page,
            extra=extra, **kwargs,
        )

    def hoyolab_xrpc5_headers(
        self, ds: str, cookie: str, device_id: str, page: str,
        extra: Dict[str, str] = {},
        **kwargs: str,
    ):
        return self.hoyolab_headers(
            ds=ds, origin='https://webstatic.mihoyo.com/',
            referer='https://webstatic.mihoyo.com/', cookie=cookie,
            client_type='5', device_id=device_id, page=page,
            extra=extra, **kwargs,
        )

    def get_cached_device_fp(self, device_id: str) -> str:
        fp = HoyolabClient.device_fp_cache.get(device_id)
        if fp is not None:
            return str(fp)  # for type annotation compatibility
        fp = self.get_device_fingerprint(device_id=device_id)
        HoyolabClient.device_fp_cache.set(device_id, fp)
        return fp

    @enter()
    def get_device_fingerprint(self, device_id: str) -> str:
        headers = {
            'Origin': 'https://webstatic.mihoyo.com/',
            'Referer': 'https://webstatic.mihoyo.com/',
            'User-Agent': HoyolabClient.user_agent,
            'x-rpc-app_version': HoyolabClient.xrpc_version,
            'x-rpc-client_type': '5',
        }
        params = {
            'app_name': 'account_cn',
            'device_id': device_id,
            'device_fp': random_hexstring(13),
            'platform': '5',
            'seed_id': random_hexstring(16),
            'seed_time': str(round(time.time() * 1000)),
            'ext_fields': (
                '{'
                f'"userAgent":"{HoyolabClient.user_agent}",'
                '"browserScreenSize":329280,'
                '"maxTouchPoints":5,'
                '"isTouchSupported":true,'
                '"browserLanguage":"zh-CN",'
                '"browserPlat":"Linux i686",'
                '"browserTimeZone":"Asia/Shanghai",'
                '"webGlRender":"Adreno (TM) 640",'
                '"webGlVendor":"Qualcomm",'
                '"numOfPlugins":0,'
                '"listOfPlugins":"unknown",'
                '"screenRatio":3.75,'
                '"deviceMemory":"4",'
                '"hardwareConcurrency":"4",'
                '"cpuClass":"unknown",'
                '"ifNotTrack":"unknown",'
                '"ifAdBlock":0,'
                '"hasLiedResolution":1,'
                '"hasLiedOs":0,'
                '"hasLiedBrowser":0'
                '}'
            ),
        }
        try:
            payload = self.request_json(
                method='post',
                url=api.device_fingerprint,
                params=params,
                headers=headers,
                timeout=10,
            )
            return payload['data']['device_fp']
        except Exception:
            logger.error(traceback.format_exc())
            return random_hexstring(13)

    @enter()
    def get_multi_token_by_login_ticket(
        self,
        login_ticket: str,
        login_uid: str,
    ) -> Optional[Dict[str, str]]:
        headers = self.xrpc5_headers(device_id='')
        params = {
            'login_ticket': login_ticket,
            'uid': login_uid,
            'token_types': '3',
        }
        try:
            payload = self.request_json(
                method='get',
                url=api.get_multi_token_by_login_ticket,
                params=params,
                headers=headers,
                timeout=10,
            )
            for item in payload['data']['list']:
                if isinstance(item, dict) and 'name' in item:
                    if item['name'].lower() == 'ltoken':
                        ltoken = item['token']
                    if item['name'].lower() == 'stoken':
                        stoken = item['token']
            return {
                'ltoken': ltoken,
                'stoken': stoken,
            }
        except Exception:
            logger.error(traceback.format_exc())
            return None

    @enter()
    def get_v2token_by_stoken(
        self,
        v1stoken: str,
        v1uid: str,
    ) -> Optional[Dict[str, str]]:
        cookie = f'stuid={v1uid};stoken={v1stoken}'
        device_id = str(uuid.uuid4())
        ds = dynamic_secret.DynamicSecretGenerator(
            version=dynamic_secret.DynamicSecretVersion.V2,
            salt_type=dynamic_secret.SaltType.PROD,
            include_chars=True,
        ).generate(
            content=cookie,
            url=api.get_v2token_by_stoken,
        )
        headers = self.xrpc2_headers(
            device_id=device_id,
            Cookie=cookie,
            DS=ds,
        )
        try:
            payload = self.request_json(
                method='post',
                url=api.get_v2token_by_stoken,
                headers=headers,
                timeout=10,
            )
            return {
                'token': payload['data']['token']['token'],
                'aid': payload['data']['user_info']['aid'],
                'mid': payload['data']['user_info']['mid'],
                'device_id': device_id,
            }
        except Exception:
            logger.error(traceback.format_exc())
            return None

    @enter()
    def get_cookie_token_by_game_token(
        self,
        game_token: str,
        aid: str,
        device_id: str,
    ) -> Optional[str]:
        params = {
            'game_token': game_token,
            'account_id': aid,
        }
        headers = self.xrpc5_headers(device_id=device_id)
        try:
            payload = self.request_json(
                method='get',
                url=api.get_cookie_by_game_token,
                headers=headers,
                params=params,
                timeout=10,
            )
            return payload['data']['cookie_token']
        except Exception:
            logger.error(traceback.format_exc())
            return None

    @enter()
    def get_cookie_token_by_stoken(
        self,
        v2stoken: str,
        aid: str,
        mid: str,
        device_id: str,
    ) -> Optional[str]:
        cookie = f'stuid={aid};stoken={v2stoken};mid={mid}'
        ds = dynamic_secret.DynamicSecretGenerator(
            version=dynamic_secret.DynamicSecretVersion.V2,
            salt_type=dynamic_secret.SaltType.PROD,
            include_chars=True,
        ).generate(
            content=cookie,
            url=api.get_cookie_by_stoken,
        )
        headers = self.xrpc2_headers(
            device_id=device_id,
            Cookie=cookie,
            DS=ds,
        )
        try:
            payload = self.request_json(
                method='get',
                url=api.get_cookie_by_stoken,
                headers=headers,
                timeout=10,
            )
            return payload['data']['cookie_token']
        except Exception:
            logger.error(traceback.format_exc())
            return None

    @enter()
    def get_stoken_by_game_token(
        self,
        game_token: str,
        aid: str,
        device_id: str,
    ):
        params = {
            'account_id': aid,
            'game_token': game_token,
        }
        ds = dynamic_secret.DynamicSecretGenerator(
            version=dynamic_secret.DynamicSecretVersion.V2,
            salt_type=dynamic_secret.SaltType.PROD,
            include_chars=True,
        ).generate(
            content=params,
            url=api.get_stoken_by_game_token,
        )
        headers = self.xrpc11_headers(
            device_id=device_id,
            DS=ds,
        )
        try:
            payload = self.request_json(
                method='post',
                url=api.get_stoken_by_game_token,
                params=params,
                headers=headers,
                timeout=10,
            )
            return {
                'stoken': payload['data']['token']['token'],
                'mid': payload['data']['user_info']['mid'],
            }
        except Exception:
            logger.error(traceback.format_exc())
            return None

    @enter()
    def get_game_record_card(
        self,
        cookie_token: str,
        aid: str,
        role_id: str,
        device_id: str,
    ):
        cookie = f'account_id={aid};cookie_token={cookie_token}'
        params = {'uid': aid}
        query_str = f'uid={aid}&role_id={role_id}&server=prod_gf_cn'
        ds = dynamic_secret.DynamicSecretGenerator(
            version=dynamic_secret.DynamicSecretVersion.V1,
            salt_type=dynamic_secret.SaltType.X4,
            include_chars=False,
        ).generate(query=query_str)
        headers = self.hoyolab_xrpc5_headers(
            ds=ds, cookie=cookie, device_id=device_id, page='',
        )
        try:
            payload = self.request_json(
                method='get',
                url=api.game_record,
                params=params,
                headers=headers,
                timeout=10,
            )
            return payload
        except Exception:
            logger.error(traceback.format_exc())
            return None

    @enter()
    def get_login_qrcode(self) -> Optional[Dict[str, str]]:
        device_id = str(uuid.uuid4())
        params = dict(app_id='8', device=device_id)
        try:
            payload = self.request_json(
                method='post',
                url=api.qrcode_fetch,
                params=params,
                timeout=10,
            )
            url = payload['data']['url']
            query_dict = parse_qs(urlparse(url).query)
            ticket = query_dict['ticket'][0]
            return {
                'app_id': '8',
                'ticket': ticket,
                'device': device_id,
                'url': url,
            }
        except Exception:
            logger.error(traceback.format_exc())
            return None

    @enter()
    def check_login_qrcode(
        self,
        app_id: str,
        ticket: str,
        device: str,
    ):
        params = dict(app_id=app_id, ticket=ticket, device=device)
        try:
            payload = self.request_json(
                method='post',
                url=api.qrcode_query,
                params=params,
                timeout=10,
            )
            return payload
        except Exception:
            logger.error(traceback.format_exc())
            return None
