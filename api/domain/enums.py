from enum import Enum, IntEnum, unique
from http.client import TOO_MANY_REQUESTS
from sre_constants import SUCCESS


@unique
class CountryCode(Enum):
    ARGENTINA = "ar"
    COLOMBIA = "co"
    MEXICO = "mx"


@unique
class PlatformCode(Enum):
    CABIFY = "cabify"
    INDRIVER = "indriver"
    RAPPI = "rappi"
    PEDIDOSYA = "pedidosya"


@unique
class UserPurpose(Enum):
    CHANGE_BANK_ACCOUNT = "change_bank_account"


@unique
class Source(Enum):
    WIDGET = "widget"


@unique
class AppLoginStatus(Enum):
    CREATED = "created"
    READY_TO_VERIFY = "ready_to_verify"
    SUCCESS = "success"
    FAILED = "failed"


@unique
class AppLoginFailedReason(Enum):
    CREDENTIALS_INVALID = "credentials_invalid"
    TOO_MANY_REQUESTS = "too_many_requests"
    TIMED_OUT = "timed_out"


@unique
class PlatformStatus(Enum):
    OPERATING = "available"
    NOT_OPERATING = "unavailable"
    SOON_TO_OPERATE = "soon_to_operate"
