from enum import Enum


class QrcodeStatus(Enum):

    INITIAL = 'Init'

    SCANNED = 'Scanned'

    CONFIRMED = 'Confirmed'
