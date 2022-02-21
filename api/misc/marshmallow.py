from marshmallow import (
    ValidationError,
    fields,
)

import phonenumbers
from .entities import PhoneNumber


class PhoneField(fields.Field):
    """Field to validate a phone number format on a request"""

    def _deserialize(self, value, *args, **kwargs) -> PhoneNumber:
        try:
            phone_parsed = phonenumbers.parse(value)
            if not phonenumbers.is_valid_number(phone_parsed):
                raise ValidationError("The format of the phone number is not valid")
            return PhoneNumber(
                country_code=str(phone_parsed.country_code),
                national_number=str(phone_parsed.national_number),
            )
        except Exception as e:
            raise ValidationError(
                "The phone number must follow an international format"
            ) from e
