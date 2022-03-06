import datetime

import pytest

from api.data.fakers import (
    AppLoginPostgresFaker,
    ClientPostgresFaker,
    PlatformPostgresFaker,
    UserPostgresFaker,
)
from api.data.postgres_models import UserPostgres
from api.data.postgres_repositories import (
    repo_create_app_login,
    repo_create_user,
    repo_get_client_by_api_key,
    repo_get_latest_user_app_login,
    repo_get_platform_by_code,
    repo_get_user_by_client_and_user,
)
from api.domain.entities import AppLogin, Client, Platform, User
from api.domain.enums import AppLoginStatus, CountryCode, PlatformCode
from api.domain.exceptions import NotFoundException
from api.misc.utils import create_cuid


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
            client_id=mock_user.client.id, user_cuid=mock_user.cuid
        )

        assert isinstance(user, User)
        assert mock_user.id == user.id

    @pytest.mark.asyncio
    async def test_repo_get_user_by_client_and_user_not_found(self):

        user = await repo_get_user_by_client_and_user(client_id=1, user_cuid="id_")

        assert user is None

    @pytest.mark.asynciorepo_get_user_by_client_and_user
    async def test_repo_create_user(self):
        cuid = 1
        mock_client = await ClientPostgresFaker.create()
        client = Client(
            id=mock_client.id,
            email="jane.doe@gmail.com",
            api_key="api_key",
            company_name="Company Name",
            cuid="cuid",
            logo_url="https://palenca.com/image.webm",
            platforms=[PlatformCode.INDRIVER.value],
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )

        user = await repo_create_user(client=client, user_cuid=cuid)

        assert isinstance(user, User)
        assert user.client.id == client.id

    @pytest.mark.asyncio
    async def test_repo_get_latest_user_app_login(self):
        user_id = 55
        platform = PlatformCode.PEDIDOSYA
        login = "jane.doe@gmail.com"

        user = await UserPostgresFaker.create(id=user_id)
        client = await ClientPostgresFaker.create()

        await AppLoginPostgresFaker.create(
            user=user, platform=platform.value, login=login, client=client
        )
        await AppLoginPostgresFaker.create()

        app_login = await repo_get_latest_user_app_login(
            user_id=user_id,
            platform=platform,
            login=login,
        )

        assert isinstance(app_login, AppLogin)
        assert app_login.user_id == user_id

    @pytest.mark.asyncio
    async def test_repo_create_app_login(self):
        user_id = 33
        client_id = 2

        await UserPostgresFaker.create(id=user_id)
        await ClientPostgresFaker.create(id=client_id)

        to_create = AppLogin(
            client_id=client_id,
            user_id=user_id,
            country=CountryCode.MEXICO,
            platform=PlatformCode.PEDIDOSYA,
            login="jane.doe@gmail.com",
            status=AppLoginStatus.CREATED,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow(),
        )
        app_login = await repo_create_app_login(app_login=to_create)

        assert isinstance(app_login, AppLogin)
        assert app_login.client_id == client_id
        assert app_login.user_id == user_id

    @pytest.mark.asyncio
    async def test_repo_get_platform_by_code(self):
        code = PlatformCode.PEDIDOSYA
        await PlatformPostgresFaker.create(code=code.value)

        platform = await repo_get_platform_by_code(code=code)

        assert isinstance(platform, Platform)
        assert platform.code == code
