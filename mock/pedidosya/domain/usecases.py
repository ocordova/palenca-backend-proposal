from mock.misc.credentials import VALID_EMAIL_PASSWORD_CREDENTIALS
from mock.pedidosya.domain.entities import Authentication
from mock.pedidosya.domain.exceptions import UnauthorizedException
from mock.pedidosya.domain.fakers import AuthenticationFactory


def pedidos_ya_login(email: str, password: str) -> Authentication:

    if {"email": email, "password": password} in VALID_EMAIL_PASSWORD_CREDENTIALS:
        mock = AuthenticationFactory.build()
        return Authentication(
            city_id=mock.city_id,
            city_name=mock.city_id,
            token=mock.token,
            contract_type=mock.contract_type,
            id_verification_required=mock.id_verification_required,
        )
    else:
        raise UnauthorizedException()
