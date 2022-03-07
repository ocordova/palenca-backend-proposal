from ..domain.enums import CountryCode
from ..misc.http import HTTPClient
from ..domain.exceptions import (
    UnauthorizedException,
    InvalidCredentialsException,
    PlatformConnectivityException,
)


async def repo_pedidosya_login(
    *, country: CountryCode, email: str, password: str
) -> None:
    url = f"https://{country.value}.usehurrier.com/api/mobile/auth"

    headers = {
        "Accept": "*/*",
        "Time-Zone": "America/Mexico_City",
        "Content-Type": "application/json",
        "User-Agent": "Roadrunner/IOS/194/3.2201.2",
    }

    body = {
        "user": {
            "user_name": email,
            "password": password,
        }
    }

    try:
        # TODO: Missing typing
        response = HTTPClient.post(url=url, headers=headers, body=body)
    except Exception as e:

        if e is UnauthorizedException:
            raise InvalidCredentialsException()

        else:
            raise PlatformConnectivityException()

    return response
