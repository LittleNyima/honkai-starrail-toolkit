from starrail.utils.loggings import get_logger

logger = get_logger(__file__)


class Locale:

    lang = 'zhs'

    available_lang = {'en', 'zhs'}


def setup_locale(lang):
    if lang not in Locale.available_lang:
        logger.warn(
            f'{lang} is not an available language, which may cause '
            'unexpected outputs',
        )
    Locale.lang = lang
