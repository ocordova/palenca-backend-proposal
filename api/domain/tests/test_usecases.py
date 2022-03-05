import pytest
from hypothesis import given, settings
from unittest.mock import patch

from api.domain.entities import AppLogin, Client, User
from api.domain.usecases import create_or_get_user, create_or_get_app_login
from api.domain.enums import CountryCode, PlatformCode, Source

from api.domain.tests.strategies import user_builder, app_login_builder, client_builder


@settings(max_examples=10)
@given(user=user_builder())
async def test_create_or_get_user_with_existent_user(user):
    with patch(
        "api.domain.usecases.repo_get_user_by_client_and_user",
        autospec=True,
        spec_set=True,
        return_value=user,
    ) as existent_user, patch(
        "api.domain.usecases.repo_create_user",
        autospec=True,
        spec_set=True,
        return_value=None,
    ) as created_user:

        result = await create_or_get_user(client=user.client, user_cuid=user.cuid)

        assert isinstance(result, User)
        assert result == user
        existent_user.assert_called_once()
        created_user.assert_not_called()


@settings(max_examples=10)
@given(user=user_builder())
async def test_create_or_get_user_without_an_existen_user(user):
    with patch(
        "api.domain.usecases.repo_get_user_by_client_and_user",
        autospec=True,
        spec_set=True,
        return_value=None,
    ) as existent_user, patch(
        "api.domain.usecases.repo_create_user",
        autospec=True,
        spec_set=True,
        return_value=user,
    ) as created_user:

        result = await create_or_get_user(client=user.client, user_cuid=user.cuid)

        assert isinstance(result, User)
        assert result == user
        existent_user.assert_called_once()
        created_user.assert_called_once()


@settings(max_examples=10)
@given(
    app_login=app_login_builder(client_id=11, user_id=34),
    user=user_builder(id=34),
    client=client_builder(id=11),
)
async def test_create_or_get_app_login_get_latest(app_login, user, client):
    with patch(
        "api.domain.usecases.repo_get_latest_user_app_login",
        autospec=True,
        spec_set=True,
        return_value=app_login,
    ) as latest_app_login, patch(
        "api.domain.usecases.repo_create_app_login",
        autospec=True,
        spec_set=True,
        return_value=None,
    ) as create_app_login:

        result = await create_or_get_app_login(
            client=client,
            user=user,
            country=app_login.country,
            platform=app_login.platform,
            login=app_login.login,
            password=app_login.password,
        )

        assert isinstance(result, AppLogin)
        assert app_login == result
        latest_app_login.assert_called_once()
        create_app_login.assert_not_called()


@settings(max_examples=10)
@given(
    app_login=app_login_builder(client_id=11, user_id=34),
    user=user_builder(id=34),
    client=client_builder(id=11),
)
async def test_create_or_get_app_login_create(app_login, user, client):
    with patch(
        "api.domain.usecases.repo_get_latest_user_app_login",
        autospec=True,
        spec_set=True,
        return_value=None,
    ) as latest_app_login, patch(
        "api.domain.usecases.repo_create_app_login",
        autospec=True,
        spec_set=True,
        return_value=app_login,
    ) as create_app_login:

        result = await create_or_get_app_login(
            client=client,
            user=user,
            country=CountryCode.COLOMBIA,
            platform=PlatformCode.PEDIDOSYA,
            login=app_login.login,
            password=app_login.password,
            worker_id=app_login.worker_id,
            source=app_login.source,
        )

        assert isinstance(result, AppLogin)
        assert result.login == app_login.login
        assert result.password == app_login.password
        assert result.worker_id == app_login.worker_id
        assert result.source == app_login.source
        latest_app_login.assert_called_once()
        create_app_login.assert_called_once()
