from api.domain.entities import PlatformJWTLogin
from mock.pedidosya.presentation.responses import SucessfullLogin


def pedidos_ya_login_adapter(*, sucessful_login: SucessfullLogin) -> PlatformJWTLogin:
    return PlatformJWTLogin(jwt_token=sucessful_login.token)
