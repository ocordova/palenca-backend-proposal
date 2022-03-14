from fastapi import APIRouter, Depends, status

from mock.pedidosya.domain.usecases import pedidos_ya_login
from mock.pedidosya.presentation.responses import SucessfullLogin
from mock.pedidosya.presentation.validations import LoginBody

pedidosya_router = APIRouter(tags=["pedidosya"])


@pedidosya_router.post(
    "/login",
    tags=["pedidosya"],
    summary="PedidosYaLogin",
    description="PedidosYa Login authentication",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SucessfullLogin},
    },
)
async def post_pedidosya_login(*, body: LoginBody):
    authentication = pedidos_ya_login(
        email=body.user.user_name, password=body.user.password
    )
    return SucessfullLogin(
        token=authentication.token,
        contract_type=authentication.contract_type,
        id_verification_required=authentication.id_verification_required,
        city_id=authentication.city_id,
        city_name=authentication.city_name,
    )
