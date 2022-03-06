from fastapi import APIRouter, Depends, status

from ..domain.entities import Client
from ..domain.enums import PlatformCode
from ..domain.usecases import pedidosya_create_user
from ..misc.fastapi import auth_with_api_key
from .responses import HealthResponse, OTPSentSuccessfullyResponse
from .validations import PedidosYaCreateUserBody

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


@pedidosya_router.post(
    "/create-user",
    summary="Create pedidos ya user",
    description="Endpoint to create a new pedidos ya user",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": OTPSentSuccessfullyResponse}},
)
async def post_pedidosya_create_user(
    *, body: PedidosYaCreateUserBody, auth_client: Client = Depends(auth_with_api_key)
):
    user = await pedidosya_create_user(
        user_cuid=body.cuid,
        email=body.email,
        password=body.password,
        country=body.country,
        auth_client=auth_client,
        source=body.source,
        worker_id=body.worker_id,
    )
    return user
