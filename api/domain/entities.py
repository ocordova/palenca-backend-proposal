import datetime
from pydantic import BaseModel
from typing import Dict, List, Optional
from .enums import Platform


class ClientExtraData(BaseModel):
    redirect_url: Optional[str]
    sheet_id: Optional[str]


class Client(BaseModel):
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


class UserExtraData(BaseModel):
    something: str


class User(BaseModel):
    id: int
    user_id: str
    client: Client
    created_at: datetime.datetime
    updated_at: datetime.datetime
    extra_data: Optional[UserExtraData] = None
