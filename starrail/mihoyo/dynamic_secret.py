import json
import random
import time
from enum import Enum
from typing import Optional
from urllib.parse import unquote, urlparse

from starrail.utils.security import MD5


class DynamicSecretVersion(Enum):
    """Hoyolab dynamic secret versions."""

    V1 = 1

    V2 = 2


class SaltType(Enum):
    """Hoyolab salt types. (v2.67.1)"""

    NONE = ''

    K2 = 'yajbb9O8TgQYOW7JVZYfUJhXN7mAeZPE'

    LK2 = 'LyD1rXqMv2GJhnwdvCBjFOKGiKuLY3aO'

    X4 = 'xV8v4Qu54lUKrEYFZkJhB8cuOh9Asafs'

    X6 = 't0qEgfub6cvueAPgR5m9aQWWVciEer7v'

    PROD = 'JwYDpKvLj6MrMqqYU6jTKF17KNO2PXoS'


class DynamicSecretGenerator:
    """
    Dynamic secret generator for Hoyolab.

    Attributes:
        version (DynamicSecretVersion): The version of the dynamic secret.
        salt_type (SaltType): The type of salt to use in the dynamic secret.
        include_chars (bool): Whether to include characters in the random
            string component.
    """

    def __init__(
        self,
        version: DynamicSecretVersion,
        salt_type: SaltType,
        include_chars: bool,
    ):
        self.version = version
        self.salt_type = salt_type
        self.include_chars = include_chars

    @property
    def default_body(self):
        """
        Returns the default body to use based on the salt type.

        Returns:
            str: The default body string.
        """

        return '{}' if self.salt_type == SaltType.PROD else ''

    @staticmethod
    def dumps(obj):
        if isinstance(obj, str):
            return obj
        return json.dumps(obj)

    def random_str(self):
        """
        Generate a random string based on the include_chars attribute.

        Returns:
            str: The generated random string.
        """

        if self.include_chars:
            return self._random_str_with_chars()
        return self._random_str_no_chars()

    def _random_str_with_chars(self):
        """
        Generate a random string containing supported characters.

        Returns:
            str: The generated random string with characters.
        """

        supported_chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
        return ''.join(random.choice(supported_chars) for _ in range(6))

    def _random_str_no_chars(self):
        """
        Generate a random string containing only numbers.

        Returns:
            str: The generated random string without characters.
        """

        rand = random.randint(100000, 200000)
        return '642367' if rand == 100000 else str(rand)

    def generate(
        self,
        content=None,
        url: Optional[str] = None,
        query: Optional[str] = None,
    ):
        """
        Generate a dynamic secret based on the input content and URL.

        Args:
            content: The content to include in the dynamic secret.
            url (str): The URL to process.

        Returns:
            str: The generated dynamic secret.
        """

        salt = self.salt_type.value
        t = int(time.time())
        r = self.random_str()

        dscontent = f'salt={salt}&t={t}&r={r}'

        if self.version == DynamicSecretVersion.V2:
            body = self.dumps(content) if content else self.default_body
            if query:
                query_str = query
            elif url:
                query_str = urlparse(unquote(url)).query
                query_str = '&'.join(sorted(query_str.split('&')))
            else:
                query_str = ''
            dscontent += f'&b={body}&q={query_str}'

        check = MD5.hash(dscontent)
        return f'{t},{r},{check}'
