from mock.pedidosya.presentation.responses import SucessfullLogin
from api.domain.entities import PlatformJWTLogin


def pedidos_ya_login_adapter(*, login: SucessfullLogin) -> PlatformJWTLogin:
    return PlatformJWTLogin(jwt_token=login["token"])
