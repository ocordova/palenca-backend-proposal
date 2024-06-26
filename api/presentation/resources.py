from fastapi import APIRouter, Depends, status

from api.domain.entities import Client
from api.domain.enums import PlatformCode
from api.domain.usecases import pedidosya_create_user
from api.misc.fastapi import auth_with_api_key
from api.presentation.responses import (
    CreateUserExceptionResponse,
    HealthResponse,
    SucessfullLoginResponse,
)
from api.presentation.validations import PedidosYaCreateUserBody

PEDIDOSYA_URI = PlatformCode.PEDIDOSYA.value

health_router = APIRouter(prefix="/health", tags=["health"])
pedidosya_router = APIRouter(prefix=f"/{PEDIDOSYA_URI}", tags=[f"{PEDIDOSYA_URI}"])


@health_router.get(
    "/",
    tags=["health"],
    summary="Get health check",
    description="Checks whether the application server is running.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": HealthResponse},
    },
)
def get_health_check_resource():
    return HealthResponse(status=status.HTTP_200_OK)


# TODO: Find a way to return multiple examples from one status
@pedidosya_router.post(
    "/create-user",
    summary="Create pedidos ya user",
    description="Endpoint to create a new pedidos ya user",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {"model": SucessfullLoginResponse},
        status.HTTP_400_BAD_REQUEST: {"model": CreateUserExceptionResponse},
    },
)
# TODO Try to use a decorator instead of the Depends, but it needs to be detected by the swagger generator
async def post_pedidosya_create_user(
    *, body: PedidosYaCreateUserBody, auth_client: Client = Depends(auth_with_api_key)
):
    user = await pedidosya_create_user(
        user_cuid=body.user_id,
        email=body.email,
        password=body.password,
        country=body.country,
        auth_client=auth_client,
        source=body.source,
        worker_id=body.worker_id,
    )
    return SucessfullLoginResponse(user_id=user.cuid)
