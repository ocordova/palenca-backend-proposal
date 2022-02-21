from decimal import Decimal
from marshmallow import EXCLUDE, Schema, fields
from marshmallow_enum import EnumField
from ..misc.marshmallow import PhoneField

from ..domain.enums import CountryCode


class IndriverCreateUserValidation(Schema):
    user_id = fields.Str(required=True)
    phone_number = PhoneField(required=True)
    country = EnumField(CountryCode, required=True)

    class Meta:
        unknown = EXCLUDE
