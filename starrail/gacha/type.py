from enum import Enum


class GachaType(Enum):
    """
    Enumeration class representing the various types of gacha types.

    Attributes:
        STELLAR (int): Value representing the Stellar Event Warp.
        DEPARTURE (int): Value representing the Departure Event Warp.
        CHARACTER (int): Value representing the Character Event Warp.
        LIGHT_CONE (int): Value representing the Light Cone Event Warp.
    """

    STELLAR = 1
    DEPARTURE = 2
    CHARACTER = 11
    LIGHT_CONE = 12
