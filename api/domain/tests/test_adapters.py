import pytest

from api.data.fakers import (
    AppLoginPostgresFaker,
    ClientPostgresFaker,
    PlatformPostgresFaker,
    UserPostgresFaker,
)
from api.domain.adapters import (
    app_login_postgres_adapter,
    client_postgres_adapter,
    platform_postgres_adapter,
    user_postgres_adapter,
)
from api.domain.entities import (
    AppLogin,
    AppLoginExtraData,
    Client,
    ClientExtraData,
    Platform,
    User,
    UserExtraData,
)
from api.domain.enums import UserPurpose


@pytest.mark.asyncio
async def test_client_postgres_adapter():

    client = await ClientPostgresFaker.create()

    entity = client_postgres_adapter(client=client)

    assert isinstance(entity, Client)
    assert entity.id == client.id
    assert entity.email == client.email
    assert entity.api_key == client.api_key
    assert entity.company_name == client.company_name
    assert entity.cuid == client.cuid
    assert entity.logo_url == client.logo_name
    assert list(map(lambda p: p.value, entity.platforms)) == client.list_apps
    assert isinstance(entity.extra_data, ClientExtraData)
    assert entity.created_at == client.created_at
    assert entity.updated_at == client.updated_at
    assert entity.webhook_url == client.webhook_url


@pytest.mark.asyncio
async def test_user_postgres_adapter():

    user = await UserPostgresFaker.create()

    entity = user_postgres_adapter(user=user)
    assert isinstance(entity, User)
    assert entity.id == user.id
    assert entity.cuid == user.cuid
    assert isinstance(entity.client, Client)
    assert isinstance(entity.extra_data, UserExtraData)
    assert entity.extra_data.purpose == UserPurpose(user.extra_data.get("purpose"))
    assert entity.created_at == user.created_at
    assert entity.updated_at == user.updated_at


@pytest.mark.asyncio
async def test_app_login_postgres_adapter():

    app_login = await AppLoginPostgresFaker.create()

    entity = app_login_postgres_adapter(app_login=app_login)
    assert isinstance(entity, AppLogin)
    assert entity.id == app_login.id
    assert entity.client_id == app_login.client_id
    assert entity.user_id == app_login.user_id
    assert entity.login == app_login.login
    assert entity.password == app_login.password
    assert entity.country.value == app_login.country
    assert entity.platform.value == app_login.platform
    assert entity.source.value == app_login.source
    assert entity.worker_id == app_login.worker_id
    assert entity.status.value == app_login.status
    assert entity.failed_reason.value == app_login.failed_reason
    assert entity.access_token == app_login.access_token
    assert entity.refresh_token == app_login.refresh_token
    assert entity.expiration_date == app_login.expiration_date
    assert entity.created_at == app_login.created_at
    assert entity.updated_at == app_login.updated_at
    assert isinstance(entity.extra_data, AppLoginExtraData)


@pytest.mark.asyncio
async def test_platform_postgres_adapter():

    platform = await PlatformPostgresFaker.create()
    entity = platform_postgres_adapter(platform=platform)

    assert isinstance(entity, Platform)
    assert entity.id == platform.id
    assert entity.code.value == platform.code
    assert entity.status.value == platform.status
    assert (
        list(map(lambda c: c.value, entity.available_countries))
        == platform.available_countries
    )
    assert entity.created_at == platform.created_at
    assert entity.updated_at == platform.updated_at
