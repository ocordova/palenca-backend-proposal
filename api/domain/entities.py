import datetime

from pydantic import BaseModel

from api.domain.enums import (
    AppLoginFailedReason,
    AppLoginStatus,
    CountryCode,
    PlatformCode,
    PlatformStatus,
    Source,
    UserPurpose,
)


class ClientExtraData(BaseModel):
    redirect_url: str | None = None
    sheet_id: str | None = None


class Client(BaseModel):
    id: int
    cuid: str
    email: str
    api_key: str
    company_name: str
    logo_url: str
    platforms: list[PlatformCode]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    webhook_url: str | None = None
    extra_data: ClientExtraData | None = None


class UserExtraData(BaseModel):
    purpose: UserPurpose | None = None


class User(BaseModel):
    id: int
    cuid: str
    client: Client
    created_at: datetime.datetime
    updated_at: datetime.datetime
    extra_data: UserExtraData | None = None


class AppLoginExtraData(dict):
    key: str | None = None


class AppLogin(BaseModel):
    client_id: int
    user_id: int
    country: CountryCode
    platform: PlatformCode
    login: str
    status: AppLoginStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: int | None = None
    password: str | None = None
    worker_id: str | None = None
    source: Source | None = None
    failed_reason: AppLoginFailedReason | None = None
    expiration_date: datetime.datetime | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    extra_data: AppLoginExtraData | None = None


class Platform(BaseModel):
    id: int
    code: PlatformCode
    status: PlatformStatus
    available_countries = [CountryCode]
    created_at: datetime.datetime
    updated_at: datetime.datetime


class PlatformJWTLogin(BaseModel):
    jwt_token: str
