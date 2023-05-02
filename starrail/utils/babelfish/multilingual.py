from typing import Dict

from starrail.utils.babelfish.locale import Locale
from starrail.utils.loggings import get_logger

logger = get_logger(__file__)


class MultilingualString:

    def __init__(self, **kwargs: str):
        self.mapping: Dict[str, str] = dict()
        for key, value in kwargs.items():
            if key not in Locale.available_lang:
                logger.warn(f'{key} is not a valid language')
            self.mapping[key] = value

    def __call__(self, *args, **kwargs):
        lang = Locale.lang
        return self.mapping[lang].format(*args, **kwargs)
