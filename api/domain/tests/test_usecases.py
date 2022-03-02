import pytest
from hypothesis import given, settings
from hypothesis.strategies import builds
from unittest.mock import patch

from api.domain.entities import Client, User
from api.domain.usecases import create_or_get_user

from api.domain.tests.strategies import user_builder


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

        result = await create_or_get_user(client=user.client, user_id=user.user_id)

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

        result = await create_or_get_user(client=user.client, user_id=user.user_id)

        assert isinstance(result, User)
        assert result == user
        existent_user.assert_called_once()
        created_user.assert_called_once()

