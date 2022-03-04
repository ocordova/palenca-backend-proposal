from pydantic import BaseModel
from typing import Optional

from ..domain.enums import CountryCode


class IndriverCreateBody(BaseModel):
    user_id: str
    country: CountryCode
    phone_number: str
    source: Optional[str] = None
