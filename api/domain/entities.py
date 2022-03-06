import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel

from .enums import (
    AppLoginFailedReason,
    AppLoginStatus,
    CountryCode,
    PlatformCode,
    PlatformStatus,
    Source,
    UserPurpose,
)


class ClientExtraData(BaseModel):
    redirect_url: Optional[str]
    sheet_id: Optional[str]


class Client(BaseModel):
    id: int
    cuid: str
    email: str
    api_key: str
    company_name: str
    logo_url: str
    platforms: List[PlatformCode]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    webhook_url: Optional[str] = None
    extra_data: Optional[ClientExtraData] = None


class UserExtraData(BaseModel):
    purpose: Optional[UserPurpose] = None


class User(BaseModel):
    id: int
    cuid: str
    client: Client
    created_at: datetime.datetime
    updated_at: datetime.datetime
    extra_data: Optional[UserExtraData] = None


class AppLoginExtraData(BaseModel):
    key: Optional[str] = None


class AppLogin(BaseModel):
    client_id: int
    user_id: int
    country: CountryCode
    platform: PlatformCode
    login: str
    status: AppLoginStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: Optional[int] = None
    password: Optional[str] = None
    worker_id: Optional[str] = None
    source: Optional[Source] = None
    failed_reason: Optional[AppLoginFailedReason] = None
    expiration_date: Optional[datetime.datetime] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    extra_data: Optional[AppLoginExtraData] = None


class Platform(BaseModel):
    id: int
    code: PlatformCode
    status: PlatformStatus
    available_countries = [CountryCode]
    created_at: datetime.datetime
    updated_at: datetime.datetime
