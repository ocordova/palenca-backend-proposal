from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

from ...domain.enums import CountryCode
from ...misc.entities import PhoneNumber


class IndriverCreateBody(BaseModel):
    user_id: str
    country: CountryCode
    phone_number: str
    # phone_number: PhoneNumber = Field(..., "Phone number of the indriver user account (e.g: 7295740734)" )
