import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional
from .enums import Platform


@dataclass
class ClientExtraData:
    redirect_url: Optional[str]
    sheet_id: Optional[str]


@dataclass
class Client:
    id: int
    email: str
    api_key: str
    company_name: str
    client_id: str
    logo_url: str
    platforms: List[Platform]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    webhook_url: Optional[str] = None
    extra_data: Optional[ClientExtraData] = None


@dataclass
class UserExtraData:
    something: str


@dataclass
class User:
    id: int
    user_id: str
    client: Client
    created_at: datetime.datetime
    updated_at: datetime.datetime
    extra_data: Optional[UserExtraData] = None
