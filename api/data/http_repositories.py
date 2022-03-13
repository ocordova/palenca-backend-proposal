from api.domain.enums import CountryCode
from api.misc.http import HTTPClient
from api.misc.config import environment
from api.domain.entities import PlatformJWTLogin
from api.domain.http_adapters import pedidos_ya_login_adapter
from api.domain.exceptions import (
    UnauthorizedException,
    InvalidCredentialsException,
    PlatformConnectivityException,
)


async def repo_pedidosya_login(
    *, country: CountryCode, email: str, password: str
) -> PlatformJWTLogin:
    url = f"https://{country.value}.usehurrier.com/api/mobile/auth"

    if environment.is_development_or_sandbox:
        url = f"{environment.MOCK_URI}/pedidosya/login"

    # Type checking with mock classes (?)
    headers = {
        "Accept": "*/*",
        "Time-Zone": "America/Mexico_City",
        "Content-Type": "application/json",
        "User-Agent": "Roadrunner/IOS/194/3.2201.2",
    }

    body = {"user": {"user_name": email, "password": password}}

    try:

        login = await HTTPClient.post(url=url, headers=headers, body=body)
        platform_login = pedidos_ya_login_adapter(login=login)

    except UnauthorizedException:
        raise InvalidCredentialsException()

    except Exception as e:
        print(e)
        raise PlatformConnectivityException()

    return platform_login
