import datetime

from api.data.http_repositories import repo_pedidosya_login
from api.data.postgres_repositories import (
    repo_create_app_login,
    repo_create_user,
    repo_get_latest_user_app_login,
    repo_get_platform_by_code,
    repo_get_user_by_client_and_user,
    repo_save_app_login_access_token,
)
from api.domain.entities import AppLogin, Client, User
from api.domain.enums import (
    AppLoginStatus,
    CountryCode,
    PlatformCode,
    PlatformStatus,
    Source,
)
from api.domain.exceptions import (
    PlatformIsNotOperatingException,
    PlatformUnavailableInCountryException,
)
from api.misc.utils import create_cuid


async def create_or_get_user(client: Client, user_cuid: str = None) -> User:
    """Get users or creates a new one if one for client_id and user_id is not found
    :param client Client: Client related to user
    :param user_cuid str: cuid of the user
    :return The User entity
    """
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
    """Get AppLogin related to user_id, platform and login (email or phone)
    :param client Client: Client related
    :param country CountryCode: Country identifier
    :param platform PlatformCode: Platform identifier
    :param login str: Email or Phone
    :param password str: Unencrypted password
    :param Optional[worker_id] str: Worker identifier
    :param Optional[source] Source: Source identifier
    :return The AppLogin entity
    """
    latest_login = await repo_get_latest_user_app_login(
        user_id=user.id, platform=platform, login=login
    )

    app_login = latest_login

    # TODO Encrypt password
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


async def check_platform_availability(
    *, code: PlatformCode, country: CountryCode
) -> None:
    """Checks if the platform is operating and if its available in the country
    :param code PlatformCode: Platform identifier
    :param country CountryCode: Country identifier
    :return None
    :raises PlatformIsNotOperatingException: In case the platform is not operating
    :raises PlatformUnavailableInCountryException: In case the platform is not available in the country
    """
    platform = await repo_get_platform_by_code(code=code)

    if platform and platform.status == PlatformStatus.NOT_OPERATING:
        raise PlatformIsNotOperatingException(documentation_url="#platform_status")

    if platform and country not in platform.available_countries:
        raise PlatformUnavailableInCountryException(
            documentation_url="#pedidosya__available_countries"
        )


async def pedidosya_create_user(
    *,
    auth_client: Client,
    user_cuid: str,
    email: str,
    password: str,
    country: CountryCode,
    worker_id: str,
    source: Source = None
) -> User:
    """Logs in to pedidos ya and saves credentials
    :param auth_client Client: Authenticated Client
    :param user_cuid str: User human readable identifiers
    :param email str: User email
    :param password str: User password
    :param country CountryCode: Country to logged in
    :param worker_id str: Worker identifier
    :param source Source: Source identifier
    :return User entity
    :raises PlatformIsNotOperatingException: In case the platform is not operating
    :raises PlatformUnavailableInCountryException: In case the platform is not available in the country
    :raises InvalidCredentialsException: If case the credentials are invalid
    :raises PlatformConnectivityException: If case something wrong happens to comunicate with the platform
    """
    await check_platform_availability(code=PlatformCode.PEDIDOSYA, country=country)
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
    # TODO: Decrypting password before using

    # Pass MyPy Optional. We probably need AppLoginJWTPAssword entity that inherits from AppLogin
    # Because we have a lot of optional/required combinations
    assert isinstance(app_login.password, str)
    login = await repo_pedidosya_login(
        country=app_login.country, email=app_login.login, password=app_login.password
    )

    await repo_save_app_login_access_token(
        app_login=app_login, access_token=login.jwt_token
    )

    return user
