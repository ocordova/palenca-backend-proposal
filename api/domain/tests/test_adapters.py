import pytest
from api.data.models import ClientPostgres, UserPostgres
from api.domain.adapters import client_postgres_adapter, user_postgres_adapter
from api.domain.entities import Client, User, ClientExtraData, UserExtraData
from api.data.fakers import ClientPostgresFaker, UserPostgresFaker
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
    assert entity.client_id == client.client_id
    assert entity.logo_url == client.logo_name
    assert list(map(lambda p: p.value, entity.platforms)) == client.list_apps
    assert entity.created_at == client.created_at
    assert entity.updated_at == client.updated_at
    assert entity.webhook_url == client.webhook_url


@pytest.mark.asyncio
async def test_user_postgres_adapter():

    user = await UserPostgresFaker.create()

    entity = user_postgres_adapter(user=user)
    assert isinstance(entity, User)
    assert entity.id == user.id
    assert entity.user_id == user.user_id
    assert isinstance(entity.client, Client)
    assert isinstance(entity.extra_data, UserExtraData)
    assert entity.extra_data.purpose == UserPurpose(user.extra_data.get("purpose"))
    assert entity.created_at == user.created_at
    assert entity.updated_at == user.updated_at
