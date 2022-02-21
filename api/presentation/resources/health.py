from fastapi import status, APIRouter

from ..responses.health import HealthResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/",
    tags=["health"],
    summary="Get health check",
    description="Checks whether the application server is running.",
    status_code=status.HTTP_200_OK,
    responses={status.HTTP_200_OK: {"model": HealthResponse}},
)
def get_health_check_resource():
    return HealthResponse(status="OK")
