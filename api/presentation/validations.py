from pydantic import BaseModel, EmailStr
from typing import Optional

from ..domain.enums import CountryCode, Source


class PedidosYaCreateUserBody(BaseModel):
    cuid: str
    country: CountryCode
    email: EmailStr
    password: str
    worker_id: str
    source: Optional[Source] = None
