import datetime
import pytest
from api.data.repositories import (
    repo_get_client_by_api_key,
    repo_get_user_by_client_and_user,
    repo_create_user,
)
from api.data.fakers import ClientPostgresFaker, UserPostgresFaker
from api.domain.entities import Client, User
from api.domain.exceptions import NotFoundException
from api.domain.enums import Platform


class TestRepository:
    @pytest.mark.asyncio
    async def test_repo_get_client_by_api_key(self):

        mock_client = await ClientPostgresFaker.create()

        client = await repo_get_client_by_api_key(api_key=mock_client.api_key)

        assert isinstance(client, Client)
        assert mock_client.api_key == client.api_key

    @pytest.mark.asyncio
    async def test_repo_get_client_by_api_key_not_found(self):

        with pytest.raises(NotFoundException):
            result = await repo_get_client_by_api_key(api_key="mock_api_key")

            assert result is None

    @pytest.mark.asyncio
    async def test_repo_get_user_by_client_and_user(self):

        mock_user = await UserPostgresFaker.create()
        user = await repo_get_user_by_client_and_user(
            client_id=mock_user.client.id, user_id=mock_user.user_id
        )

        assert isinstance(user, User)
        assert mock_user.id == user.id

    @pytest.mark.asyncio
    async def test_repo_create_user(self):
        user_id = 1
        mock_client = await ClientPostgresFaker.create()
        client = Client(
            id=mock_client.id,
            email="jane.doe@gmail.com",
            api_key="api_key",
            company_name="Company Name",
            client_id="client_id",
            logo_url="https://palenca.com/image.webm",
            platforms=[Platform.INDRIVER.value],
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        user = await repo_create_user(client=client, user_id=user_id)

        assert isinstance(user, User)
        assert user.client.id == client.id
