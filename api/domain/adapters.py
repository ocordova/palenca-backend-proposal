from ..data.models import (
    AppLoginPostgres,
    ClientPostgres,
    UserPostgres,
    PlatformPostgres,
)
from .entities import (
    AppLogin,
    Client,
    ClientExtraData,
    Platform,
    UserExtraData,
    User,
    AppLoginExtraData,
)
from .enums import AppLoginStatus, CountryCode, PlatformCode, Source, PlatformStatus


def client_postgres_adapter(*, client: ClientPostgres) -> Client:
    client_extra_data = None
    if client.extra_data is not None:
        client_extra_data = ClientExtraData(key=client.extra_data.get("key", None))

    return Client(
        id=client.id,
        email=client.email,
        api_key=client.api_key,
        company_name=client.company_name,
        cuid=client.cuid,
        logo_url=client.logo_name,
        platforms=list(map(lambda pt: PlatformCode(pt), client.list_apps)),
        webhook_url=client.webhook_url,
        created_at=client.created_at,
        extra_data=client_extra_data,
        updated_at=client.updated_at,
    )


def user_postgres_adapter(*, user: UserPostgres) -> User:
    user_extra_data = None
    if user.extra_data is not None:
        user_extra_data = UserExtraData(purpose=user.extra_data.get("purpose", None))
    return User(
        id=user.id,
        cuid=user.cuid,
        client=client_postgres_adapter(client=user.client),
        created_at=user.created_at,
        updated_at=user.updated_at,
        extra_data=user_extra_data,
    )


def app_login_postgres_adapter(*, app_login: AppLoginPostgres) -> AppLogin:
    app_login_extra_data = None
    if app_login.extra_data is not None:
        app_login_extra_data = AppLoginExtraData(
            purpose=app_login.extra_data.get("key", None)
        )
    return AppLogin(
        id=app_login.id,
        client_id=app_login.client_id,
        user_id=app_login.user_id,
        login=app_login.login,
        password=app_login.password,
        country=CountryCode(app_login.country),
        platform=PlatformCode(app_login.platform),
        source=Source(app_login.source) if app_login.source is not None else None,
        worker_id=app_login.worker_id,
        status=AppLoginStatus(app_login.status),
        failed_reason=app_login.failed_reason,
        access_token=app_login.access_token,
        refresh_token=app_login.refresh_token,
        expiration_date=app_login.expiration_date,
        created_at=app_login.created_at,
        updated_at=app_login.updated_at,
        extra_data=app_login_extra_data,
    )


def platform_postgres_adapter(*, platform: PlatformPostgres) -> Platform:
    return Platform(
        id=platform.id,
        code=PlatformCode(platform.code),
        status=PlatformStatus(platform.status),
        available_countries=list(
            map(lambda pt: CountryCode(pt), platform.available_countries)
        ),
        created_at=platform.created_at,
        updated_at=platform.updated_at,
    )
