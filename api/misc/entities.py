from dataclasses import dataclass, field


@dataclass
class PhoneNumber:
    country_code: str
    national_number: str
    international_format: str = field(init=False)

    def __post_init__(self):
        # Creates the international format of the phone number
        self.international_format = f"+{self.country_code}{self.national_number}"
