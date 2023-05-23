from starrail.utils.loggings import get_logger

logger = get_logger(__file__)


class Locale:

    lang = 'zhs'

    available_lang = {'en', 'zhs'}

    default_lang = 'zhs'


locale_mapping = {
    'en_US': 'en',
    'zh_CN': 'zhs',
}


def setup_locale(lang):
    if lang in locale_mapping:
        lang = locale_mapping[lang]
    elif lang not in Locale.available_lang:
        logger.warn(
            f'{lang} is not an available language, which may cause '
            'unexpected outputs',
        )
        logger.warn(f'Locale falls back to {Locale.default_lang}')
    Locale.lang = lang
