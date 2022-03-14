import pytest

from api.domain.entities import PlatformJWTLogin
from api.domain.http_adapters import pedidos_ya_login_adapter
from mock.pedidosya.presentation.fakers import SucessfullLoginFactory
from mock.pedidosya.presentation.responses import SucessfullLogin


@pytest.mark.asyncio
async def test_pedidos_ya_login_adapter():
    token = "token_x"
    mock: SucessfullLogin = SucessfullLoginFactory.build(token=token)

    entity = pedidos_ya_login_adapter(sucessful_login=mock)

    assert isinstance(entity, PlatformJWTLogin)
    assert entity.jwt_token == mock.token
