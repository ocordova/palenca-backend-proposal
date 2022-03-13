from unittest.mock import patch

import pytest
from mock.pedidosya.domain.usecases import pedidos_ya_login
from mock.misc.credentials import VALID_EMAIL_PASSWORD_CREDENTIALS
from mock.pedidosya.domain.entities import Authentication
from mock.pedidosya.domain.exceptions import UnauthorizedException


def test_pedidos_ya_login():
    valid = VALID_EMAIL_PASSWORD_CREDENTIALS[0]
    result = pedidos_ya_login(email=valid["email"], password=valid["password"])

    assert isinstance(result, Authentication)


def test_pedidos_ya_login_exception():
    with pytest.raises(UnauthorizedException):
        pedidos_ya_login(email="jane.doe@gmail.com", password="password")
