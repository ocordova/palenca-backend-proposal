import pytest
from api.data.models import ClientPostgres
from api.domain.adapters import client_postgres_adapter
from api.domain.entities import Client
from api.data.fakers import ClientPostgresFaker


@pytest.mark.asyncio
async def test_client_adapter():

    client = await ClientPostgresFaker.create_batch(1)
    client = await ClientPostgres.first()

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
