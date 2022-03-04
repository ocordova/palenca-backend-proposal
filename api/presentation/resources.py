from fastapi import status, APIRouter, Depends

from .responses import HealthResponse, OTPSentSuccessfullyResponse
from .validations import IndriverCreateBody
from ..domain.usecases import indriver_create_user
from ..domain.enums import Platform
from ..domain.entities import Client
from ..misc.fastapi import auth_with_api_key

INDRIVER_URI = Platform.INDRIVER.value

health_router = APIRouter(prefix="/health", tags=["health"])
indriver_router = APIRouter(prefix=f"/{INDRIVER_URI}", tags=[f"{INDRIVER_URI}"])


@health_router.get(
    "/",
    tags=["health"],
    summary="Get health check",
    description="Checks whether the application server is running.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": HealthResponse},},
)
def get_health_check_resource():
    return HealthResponse(status=status.HTTP_200_OK)


@indriver_router.post(
    "/create-user",
    summary="Create indriver user",
    description="Endpoint to create a new indriver user",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": OTPSentSuccessfullyResponse}},
)
async def post_indriver_create_user(
    *, body: IndriverCreateBody, auth_client: Client = Depends(auth_with_api_key)
):
    user = await indriver_create_user(
        user_id=body.user_id,
        phone_number=body.phone_number,
        country=body.country,
        auth_client=auth_client,
        source=body.source,
    )
    return user

