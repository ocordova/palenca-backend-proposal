from pydantic import BaseModel
from typing import Optional

from ..domain.enums import CountryCode
from ..misc.entities import PhoneNumber


class IndriverCreateBody(BaseModel):
    user_id: str
    country: CountryCode
    phone_number: str
    source: Optional[str] = None
    # phone_number: PhoneNumber = Field(..., "Phone number of the indriver user account (e.g: 7295740734)" )
