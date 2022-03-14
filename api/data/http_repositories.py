from pydantic import BaseModel, ValidationError, validator
from sentry_sdk import capture_exception

from api.domain.entities import PlatformJWTLogin
from api.domain.enums import CountryCode
from api.domain.exceptions import (
    InvalidCredentialsException,
    PlatformConnectivityException,
)
from api.domain.http_adapters import pedidos_ya_login_adapter
from api.misc.config import environment
from api.misc.http.client import HTTPClient
from api.misc.http.exceptions import UnauthorizedHTTPException
from mock.pedidosya.presentation.resources import SucessfullLogin
from mock.pedidosya.presentation.validations import LoginBody


async def repo_pedidosya_login(
    *, country: CountryCode, email: str, password: str
) -> PlatformJWTLogin:
    url = f"https://{country.value}.usehurrier.com/api/mobile/auth"

    if environment.is_development_or_sandbox:
        url = f"{environment.MOCK_URI}/pedidosya/login"

    # If we enforce the headers in the mock api, we can create the instance of that model
    headers = {
        "Accept": "*/*",
        "Time-Zone": "America/Mexico_City",
        "Content-Type": "application/json",
        "User-Agent": "Roadrunner/IOS/194/3.2201.2",
    }

    body = LoginBody(**{"user": {"user_name": email, "password": password}})

    try:
        response = await HTTPClient.post(url=url, headers=headers, body=body.dict())
        sucessful_login = SucessfullLogin(**response)
        platform_login = pedidos_ya_login_adapter(sucessful_login=sucessful_login)

    except UnauthorizedHTTPException:
        raise InvalidCredentialsException()
    except ValidationError as e:
        # This means the response from the 3rd party changed
        capture_exception(e)
        raise PlatformConnectivityException()
    except Exception as e:
        raise PlatformConnectivityException()

    return platform_login
