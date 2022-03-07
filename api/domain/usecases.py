import datetime
from os import access
from platform import platform

from ..data.postgres_repositories import (
    repo_create_app_login,
    repo_create_user,
    repo_get_latest_user_app_login,
    repo_get_platform_by_code,
    repo_get_user_by_client_and_user,
    repo_save_app_login_access_token,
)
from ..data.http_repositories import repo_pedidosya_login
from ..domain.entities import AppLogin, Client, User
from ..domain.enums import (
    AppLoginStatus,
    CountryCode,
    PlatformCode,
    PlatformStatus,
    Source,
)
from ..domain.exceptions import (
    PlatformUnavailableInCountryException,
    PlatformIsNotOperatingException,
)
from ..misc.utils import create_cuid


async def create_or_get_user(client: Client, user_cuid: str = None) -> User:

    user = None

    if not user_cuid:
        user_cuid = create_cuid()

    user = await repo_get_user_by_client_and_user(
        client_id=client.id, user_cuid=user_cuid
    )

    if not user:
        user = await repo_create_user(client=client, user_cuid=user_cuid)

    return user


async def create_or_get_app_login(
    *,
    client: Client,
    user: User,
    country: CountryCode,
    platform: PlatformCode,
    login: str,
    password: str,
    worker_id: str = None,
    source: Source = None
) -> None:

    latest_login = await repo_get_latest_user_app_login(
        user_id=user.id, platform=platform, login=login
    )

    app_login = latest_login

    if not app_login:
        to_create = AppLogin(
            client_id=client.id,
            user_id=user.id,
            country=country,
            platform=platform,
            source=source,
            worker_id=worker_id,
            login=login,
            password=password,
            status=AppLoginStatus.CREATED,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        app_login = await repo_create_app_login(app_login=to_create)

    return app_login


async def login_pedidos_ya(*, app_login: AppLogin) -> str:

    platform = await repo_get_platform_by_code(app_login.platform)

    if platform.status == PlatformStatus.NOT_OPERATING:
        raise PlatformIsNotOperatingException(documentation_url="#platform_status")

    if platform and app_login.country not in platform.available_countries:
        raise PlatformUnavailableInCountryException(
            documentation_url="#pedidosya__available_countries"
        )
    assert app_login.password is not None

    # TODO response typing
    result: dict = await repo_pedidosya_login(
        country=app_login.country, email=app_login.login, password=app_login.password
    )

    return result.access_token


async def pedidosya_create_user(
    *,
    auth_client: Client,
    user_cuid: str,
    email: str,
    password: str,
    country: CountryCode,
    source: Source = None,
    worker_id: str
) -> User:

    user = await create_or_get_user(client=auth_client, user_cuid=user_cuid)
    app_login = await create_or_get_app_login(
        client=auth_client,
        user=user,
        country=country,
        platform=PlatformCode.PEDIDOSYA,
        login=email,
        password=password,
        source=source,
        worker_id=worker_id,
    )

    response = login_pedidos_ya(app_login=app_login)

    await repo_save_app_login_access_token(
        app_login_id=app_login.id, access_token=response.access_token
    )

    return user
