from api.data.postgres_models import (
    AppLoginPostgres,
    ClientPostgres,
    PlatformPostgres,
    UserPostgres,
)
from api.domain.entities import AppLogin, Client, Platform, User
from api.domain.enums import PlatformCode
from api.domain.exceptions import NotFoundException
from api.domain.postgres_adapters import (
    app_login_postgres_adapter,
    client_postgres_adapter,
    platform_postgres_adapter,
    user_postgres_adapter,
)


async def repo_get_client_by_api_key(*, api_key: str) -> Client:
    """
    :raises: NotFoundException
    """

    client = await ClientPostgres.get_or_none(api_key=api_key)

    if client is None:
        raise NotFoundException("Client not found")

    return client_postgres_adapter(client=client)


async def repo_get_user_by_client_and_user(
    *, client_id: int, user_cuid: str
) -> User | None:
    user = await UserPostgres.get_or_none(
        cuid=user_cuid, client_id=client_id
    ).prefetch_related("client")

    if user is None:
        return None

    return user_postgres_adapter(user=user)


async def repo_create_user(*, client: Client, user_cuid: str) -> User:
    user = await UserPostgres.create(cuid=user_cuid, client_id=client.id)
    created = await user.get(id=user.id).prefetch_related("client")
    return user_postgres_adapter(user=created)


async def repo_get_latest_user_app_login(
    *, user_id: int, platform=PlatformCode, login: str
) -> AppLogin | None:
    app_login = await AppLoginPostgres.get_or_none(
        user_id=user_id, platform=platform.value, login=login
    )
    if app_login is None:
        return None

    return app_login_postgres_adapter(app_login=app_login)


async def repo_create_app_login(app_login: AppLogin) -> AppLogin:
    app_login_extra_data = {}

    if app_login.extra_data:
        app_login_extra_data["key"] = app_login.extra_data.key

    app_login_postgres = await AppLoginPostgres.create(
        client_id=app_login.client_id,
        user_id=app_login.user_id,
        country=app_login.country.value,
        platform=app_login.platform.value,
        login=app_login.login,
        password=app_login.password,
        source=app_login.source.value if app_login.source is not None else None,
        worker_id=app_login.worker_id,
        status=app_login.status.value,
        access_token=app_login.access_token,
        refresh_token=app_login.refresh_token,
        expiration_date=app_login.expiration_date,
        created_at=app_login.created_at,
        updated_at=app_login.updated_at,
        failed_reason=app_login.failed_reason,
        extra_data=app_login.extra_data,
    )

    return app_login_postgres_adapter(app_login=app_login_postgres)


async def repo_get_platform_by_code(code: PlatformCode) -> Platform | None:
    platform = await PlatformPostgres.get_or_none(code=code.value)

    if platform is None:
        return None

    return platform_postgres_adapter(platform=platform)


async def repo_save_app_login_access_token(
    app_login: AppLogin, access_token: str
) -> None:

    login = await AppLoginPostgres.get_or_none(id=app_login.id)
    login.access_token = access_token
    await login.save(update_fields=["access_token"])
