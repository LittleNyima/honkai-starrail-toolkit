import functools
import traceback
import uuid
from typing import Callable, Dict, Optional
from urllib.parse import parse_qs, urlparse

import requests

from starrail.mihoyo import api, dynamic_secret
from starrail.utils import loggings

logger = loggings.get_logger(__file__)


def enter(prefix: str = '') -> Callable:
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


class HoyolabClient:

    xrpc_version = '2.50.1'

    user_agent = 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) miHoYoBBS/2.50.1'

    def request_json(
        self,
        method,
        url,
        params=None,
        headers=None,
        timeout=None,
    ):
        logger.debug(f'requesting json: {url}')
        response = requests.request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            timeout=timeout,
        )
        payload = response.json()
        logger.debug(payload)
        return payload

    def xrpc_headers(
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

    def get_multi_token_by_login_ticket(
        self,
        login_ticket: str,
        login_uid: str,
    ) -> Optional[Dict[str, str]]:
        headers = self.xrpc_headers(device_id='')
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

    def get_cookie_token_by_stoken(
        self,
        v2stoken: str,
        uid: str,
        mid: str,
        device_id: str,
    ) -> Optional[str]:
        cookie = f'stuid={uid};stoken={v2stoken};mid={mid}'
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

    @enter(prefix='[Client]')
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

    @enter(prefix='[Client]')
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
