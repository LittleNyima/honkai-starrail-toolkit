import json
import random
import threading
import time
import traceback
import uuid
from typing import Dict, Optional
from urllib.parse import parse_qs, urlparse

import requests

from starrail.mihoyo import api
from starrail.mihoyo.codes import SaltType
from starrail.utils import loggings
from starrail.utils.security import MD5

logger = loggings.get_logger(__file__)


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


class IntervalThread(threading.Thread):

    def __init__(self, interval, callable, *args, **kwargs):
        super().__init__(deamon=True)
        self.interval = interval
        self.callable = callable
        self.args = args
        self.kwargs = kwargs
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            self.callable(*self.args, **self.kwargs)
            self.stop_event.wait(self.interval)

    def stop(self):
        self.stop_event.set()


def set_interval(interval, callable, *args, **kwargs):
    """
    Starts and returns an interval-based thread that executes the provided
    callable at each interval.

    Args:
        interval (float): The time interval between each execution of the
            callable in seconds.
        callable (Callable): The function to be executed at each interval.
        *args: Variable-length argument list to be passed to the callable.
        **kwargs: Arbitrary keyword arguments to be passed to the callable.

    Returns:
        IntervalThread: An instance of the interval-based thread.
    """

    thread = IntervalThread(interval, callable, *args, **kwargs)
    thread.start()
    return thread


def unparse_qs(query: Dict):
    return '&'.join([f'{k}={v}' for k, v in query.items()])


# Modified from GitHub code under AGPL-3.0 license:
# Mar-7th/March7th/march7th/nonebot_plugin_mys_api/api.py
class HoyolabClient:

    user_agent = (
        'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit'
        '/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.50.1'
    )

    def __init__(self):
        self.device_id = ''
        self.device_fingerprint = ''

        set_interval(300, self.refresh_device)

    def refresh_device(self):
        self.device_id = str(uuid.uuid4())
        self.device_fingerprint = self.get_device_fingerprint(self.device_id)

    @staticmethod
    def get_dynamic_secret(
        query: str = '',
        body: Optional[Dict] = None,
        salt_type: SaltType = SaltType.SALT_4X,
    ):
        """
        Generates a dynamic secret based on the given parameters.

        Args:
            query (str, optional): The query string. Defaults to ''.
            body (dict, optional): The JSON payload. Defaults to None.
            hoyolab_bbs_checkin (bool, optional): A flag that indicates
                whether to use the hoyolab_bbs_checkin secret or not. Defaults
                to False.

        Returns:
            str: The generated dynamic secret.
        """

        b = json.dumps(body) if body else ''
        s = salt_type.value
        t = str(int(time.time()))
        r = random.randint(100000, 200000)
        if r == 100000:
            r = 642367
        c = MD5.hash(f'salt={s}&t={t}&r={r}&b={b}&q={query}')
        return f'{t},{r},{c}'

    def generate_headers(
        self,
        cookie: str = '',
        query: str = '',
        body: Dict = {},
        referer: str = 'https://webstatic.mihoyo.com',
        rpc_client_type: str = '5',
        rpc_page: str = '',
        salt_type: SaltType = SaltType.SALT_4X,
    ):
        return {
            'Cookie': cookie,
            'DS': self.get_dynamic_secret(query, body, salt_type),
            'Origin': 'https://webstatic.mihoyo.com',
            'Referer': referer,
            'User-Agent': HoyolabClient.user_agent,
            'X-Requested-With': 'com.mihoyo.hyperion',
            'x-rpc-app_version': '2.50.1',
            'x-rpc-page': rpc_page,
            'x-rpc-client_type': rpc_client_type,
            'x-rpc-device_fp': self.device_fingerprint,
            'x-rpc-device_id': self.device_id,
            'x-rpc-device_name': 'iPhone14Pro',
            'x-rpc-sys_version': '12',
        }

    def get_device_fingerprint(self, device_id: str) -> str:
        """
        Retrieves the device fingerprint for the given device ID.

        Args:
            device_id (str): The device ID for which the device fingerprint
                is to be fetched.

        Returns:
            str: The device fingerprint, or a random hexadecimal string if
                fetching fails.
        """

        headers = {
            'x-rpc-app_version': '2.50.1',
            'x-rpc-client_type': '5',
            'Origin': 'https://webstatic.mihoyo.com',
            'Referer': 'https://webstatic.mihoyo.com/',
            'User-Agent': HoyolabClient.user_agent,
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
            response = requests.post(
                url=api.device_fingerprint,
                params=params,
                headers=headers,
                timeout=10,
            )
            payload = response.json()
            logger.debug(payload)
            return str(payload['data']['device_fp'])
        except Exception:
            logger.error(traceback.format_exc())
            logger.warn('Fail to get device fingerprint, using random fp.')
        return random_hexstring(13)

    def get_stoken_by_login_ticket(
            self,
            login_ticket: str,
            hoyolab_uid: str,
    ) -> str:
        headers = {
            'x-rpc-app_version': '2.50.1',
            'x-rpc-client_type': '5',
            'Origin': 'https://webstatic.mihoyo.com',
            'Referer': 'https://webstatic.mihoyo.com/',
            'User-Agent': HoyolabClient.user_agent,
        }
        params = {
            'login_ticket': login_ticket,
            'token_types': '3',
            'uid': hoyolab_uid,
        }
        try:
            response = requests.get(
                url=api.get_token_by_login_tikcet,
                params=params,
                headers=headers,
                timeout=10,
            )
            payload = response.json()
            logger.debug(payload)
            return payload['data']['list'][0]['token']
        except Exception:
            logger.error(traceback.format_exc())
            logger.warn('Fail to fetch stoken by login ticket.')
        return ''

    def get_cookie_by_stoken(self, stoken: str, hoyolab_uid: str) -> str:
        headers = {
            'x-rpc-app_version': '2.50.1',
            'x-rpc-client_type': '5',
            'Origin': 'https://webstatic.mihoyo.com',
            'Referer': 'https://webstatic.mihoyo.com/',
            'User-Agent': HoyolabClient.user_agent,
            'Cookie': f'stuid={hoyolab_uid};stoken={stoken}',
        }
        params = {
            'uid': hoyolab_uid,
            'stoken': stoken,
        }
        try:
            response = requests.get(
                url=api.get_cookie_by_stoken,
                params=params,
                headers=headers,
                timeout=10,
            )
            payload = response.json()
            logger.debug(payload)
            return payload['data']['cookie_token']
        except Exception:
            logger.error(traceback.format_exc())
            logger.warn('Fail to fetch cookie by stoken.')
        return ''

    def get_cookie_by_game_token(self, game_token: str, uid: str):
        params = {
            'game_token': game_token,
            'account_id': uid,
        }
        try:
            response = requests.get(
                url=api.get_cookie_by_game_token,
                params=params,
                timeout=10,
            )
            payload = response.json()
            logger.debug(payload)
            return payload
        except Exception:
            logger.error(traceback.format_exc())
            logger.warn('Fail to fetch cookie by game token.')
        return {}

    def get_stoken_by_game_token(self, game_token: str, uid: str):
        params = {
            'account_id': uid,
            'game_token': game_token,
        }
        headers = {
            'x-rpc-aigis': '',
            'x-rpc-game_biz': 'bbs_cn',
            'x-rpc-sys_version': '11',
            'x-rpc-device_id': self.device_id,
            'x-rpc-device_fp': self.device_fingerprint,
            'x-rpc-device_name': 'Chrome 108.0.0.0',
            'x-rpc-device_model': 'Windows 10 64-bit',
            'x-rpc-app_id': 'bll8iq97cem8',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'DS': self.get_dynamic_secret(body=params),
            'User-Agent': 'okhttp/4.8.0',
        }
        try:
            response = requests.get(
                url=api.get_stoken_by_game_token,
                params=params,
                headers=headers,
                timeout=10,
            )
            payload = response.json()
            logger.debug(payload)
            return payload
        except Exception:
            logger.error(traceback.format_exc())
            logger.warn('Fail to fetch stoken by game token.')
        return {}

    def fetch_login_qrcode(self, app_id: str) -> Dict:
        params = {
            'app_id': app_id,
            'device': self.device_id,
        }
        try:
            response = requests.get(
                url=api.qrcode_fetch,
                params=params,
                timeout=10,
            )
            payload = response.json()
            logger.debug(payload)
            url = payload['data']['url']
            parsed_url = urlparse(url)
            query_dict = parse_qs(parsed_url.query)
            ticket = query_dict.get('ticket', '')
            return {
                'app_id': app_id,
                'ticket': ticket,
                'device': self.device_id,
                'url': url,
            }
        except Exception:
            logger.error(traceback.format_exc())
            logger.warn('Fail to fetch login qrcode.')
        return {}

    def query_login_qrcode(self, login_data: Dict):
        params = {
            'app_id': login_data.get('app_id'),
            'ticket': login_data.get('ticket'),
            'device': login_data.get('device'),
        }
        try:
            response = requests.get(
                url=api.qrcode_query,
                params=params,
                timeout=10,
            )
            payload = response.json()
            logger.debug(payload)
            return payload
        except Exception:
            logger.error(traceback.format_exc())
            logger.warn('Fail to query login qrcode.')
        return {}

    def get_hoyolab_game_record(
        self,
        cookie: str,
        hoyolab_uid: str,
    ):
        params = {'uid': hoyolab_uid}
        headers = self.generate_headers(
            cookie=cookie,
            query=unparse_qs(params),
        )
        try:
            response = requests.get(
                url=api.game_record,
                params=params,
                headers=headers,
                timeout=10,
            )
            payload = response.json()
            logger.debug(payload)
            return payload['data']
        except Exception:
            logger.error(traceback.format_exc())
            logger.warn('Fail to get hoyolab game record.')
        return {}

    def get_starrail_basic_info(
        self,
        cookie: str,
        role_id: str,
    ):
        params = {
            'role_id': role_id,
            'server': 'prod_gf_cn',
        }
        headers = self.generate_headers(
            cookie=cookie,
            query=unparse_qs(params),
            rpc_page='3.7.3_#/rpg',
        )
        try:
            response = requests.get(
                url=api.hksr_basic_info,
                params=params,
                headers=headers,
                timeout=10,
            )
            payload = response.json()
            logger.debug(payload)
            return payload['data']
        except Exception:
            logger.error(traceback.format_exc())
            logger.warn('Fail to get starrail basic info.')
        return {}

    def get_starrail_index(
        self,
        cookie: str,
        role_id: str,
    ):
        params = {
            'role_id': role_id,
            'server': 'prod_gf_cn',
        }
        headers = self.generate_headers(
            cookie=cookie,
            query=unparse_qs(params),
            rpc_page='3.7.3_#/rpg',
        )
        try:
            response = requests.get(
                url=api.hksr_index,
                params=params,
                headers=headers,
                timeout=10,
            )
            payload = response.json()
            logger.debug(payload)
            return payload['data']
        except Exception:
            logger.error(traceback.format_exc())
            logger.warn('Fail to get starrail index.')
        return {}

    def get_starrail_avatar_info(
        self,
        cookie: str,
        role_id: str,
        avatar_id: str,
    ):
        params = {
            'id': avatar_id,
            'need_wiki': 'true',
            'role_id': role_id,
            'server': 'prod_gf_cn',
        }
        headers = self.generate_headers(
            cookie=cookie,
            query=unparse_qs(params),
            rpc_page='3.7.3_#/rpg/role',
            referer=(
                'https://webstatic.mihoyo.com/app/community-game-records/rpg/'
                '?bbs_presentation_style=fullscreen'
            ),
        )
        try:
            response = requests.get(
                url=api.hksr_avatar_info,
                params=params,
                headers=headers,
                timeout=10,
            )
            payload = response.json()
            logger.debug(payload)
            return payload['data']
        except Exception:
            logger.error(traceback.format_exc())
            logger.warn('Fail to get starrail avatar info.')
        return {}

    def get_starrail_note(
        self,
        cookie: str,
        role_id: str,
    ):
        params = {
            'role_id': role_id,
            'server': 'prod_gf_cn',
        }
        headers = self.generate_headers(
            cookie=cookie,
            query=unparse_qs(params),
            rpc_page='3.7.3_#/rpg',
        )
        try:
            response = requests.get(
                url=api.hksr_note,
                params=params,
                headers=headers,
                timeout=10,
            )
            payload = response.json()
            logger.debug(payload)
            return payload['data']
        except Exception:
            logger.error(traceback.format_exc())
            logger.warn('Fail to get starrail note.')
        return {}

    def get_starrail_month_info(
        self,
        cookie: str,
        role_id: str,
    ):
        params = {
            'act_id': 'e202304121516551',
            'region': 'prod_gf_cn',
            'uid': role_id,
            'lang': 'zh-cn',
        }
        headers = self.generate_headers(
            cookie=cookie,
            query=unparse_qs(params),
            rpc_page='3.7.3_#/rpg',
        )
        try:
            response = requests.get(
                url=api.hksr_month_info,
                params=params,
                headers=headers,
                timeout=10,
            )
            payload = response.json()
            logger.debug(payload)
            return payload['data']
        except Exception:
            logger.error(traceback.format_exc())
            logger.warn('Fail to get starrail month info.')
        return {}
