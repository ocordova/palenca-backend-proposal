from fastapi import status, APIRouter, Body

from ...domain.enums import Platform, CountryCode
from ...misc.entities import PhoneNumber
from ..responses.common import OTPSentSuccessfullyResponse
from ...domain.usecases.indriver import indriver_create_user
from ..validations.indriver import IndriverCreateBody

INDRIVER_URI = Platform.INDRIVER.value

router = APIRouter(prefix=f"/{INDRIVER_URI}", tags=[f"{INDRIVER_URI}"])


@router.post(
    "/create-user",
    summary="Create indriver user",
    description="Endpoint to create a new indriver user",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": OTPSentSuccessfullyResponse}},
)
async def get_health_check_resource(*, body: IndriverCreateBody):
    await indriver_create_user(
        user_id=body.user_id, phone_number=body.phone_number, country=body.country,
    )
    return OTPSentSuccessfullyResponse()
 