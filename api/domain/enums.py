from enum import Enum, IntEnum, unique


@unique
class CountryCode(Enum):
    ARGENTINA = "ar"
    COLOMBIA = "co"
    MEXICO = "mx"


@unique
class Platform(Enum):
    CABIFY = "cabify"
    INDRIVER = "indriver"
    RAPPI = "rappi"


@unique
class UserPurpose(Enum):
    CHANGE_BANK_ACCOUNT = "change_bank_account"
