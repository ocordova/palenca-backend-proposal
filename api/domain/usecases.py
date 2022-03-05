import datetime

from platform import platform

from ..domain.entities import Client, User, AppLogin
from ..domain.enums import AppLoginStatus, CountryCode, PlatformCode, Source
from ..data.repositories import (
    repo_get_platform_by_code,
    repo_get_user_by_client_and_user,
    repo_create_user,
    repo_get_latest_user_app_login,
    repo_create_app_login,
    repo_pedidosya_login,
)
from ..misc.utils import create_cuid
from ..domain.exceptions import PlatformUnavailableInCountryException


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
) -> AppLogin:

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


async def login_pedidos_ya(*, app_login: AppLogin) -> None:

    platform = await repo_get_platform_by_code(app_login.platform)

    if platform and app_login.country not in platform.available_countries:
        raise PlatformUnavailableInCountryException(
            documentation_url="#pedidosya_available_countries"
        )

    return await repo_pedidosya_login(
        country=app_login.country, email=app_login.login, password=app_login.password
    )


async def pedidosya_create_user(
    *,
    auth_client: Client,
    user_cuid: str,
    email: str,
    password: str,
    country: CountryCode,
    source: Source
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
    )

    return user
