from dataclasses import dataclass
from enum import Enum, IntEnum, unique


@unique
class CountryCode(Enum):
    ARGENTINA = "ar"
    COLOMBIA = "co"
    MEXICO = "mx"


@unique
class Platform(Enum):
    INDRIVER = "indriver"
    RAPPI = "rappi"
