from fastapi import Depends, Request, status
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader

from api.data.postgres_repositories import repo_get_client_by_api_key
from api.domain.entities import Client
from api.domain.exceptions import (
    ForbiddenException,
    NotFoundException,
    UnauthorizedException,
    TooManyRequestsException,
    InternalServerException,
    BusinessException,
)

X_API_KEY = APIKeyHeader(name="X-API-Key")

# TODO Try to use a decorator instead of the Depends, but it needs to be detected by the swagger generator
async def auth_with_api_key(api_key: str = Depends(X_API_KEY)) -> Client:

    try:
        client = await repo_get_client_by_api_key(api_key=api_key)
    except NotFoundException:
        raise UnauthorizedException(documentation_url="#authentication")

    return client


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except UnauthorizedException as e:
        return JSONResponse(
            content=e.serialize(), status_code=status.HTTP_401_UNAUTHORIZED
        )
    except NotFoundException as e:
        return JSONResponse(
            content=e.serialize(), status_code=status.HTTP_404_NOT_FOUND
        )
    except BusinessException as e:
        return JSONResponse(
            content=e.serialize(), status_code=status.HTTP_400_BAD_REQUEST
        )
    except ForbiddenException as e:
        return JSONResponse(
            content=e.serialize(), status_code=status.HTTP_403_FORBIDDEN
        )
    except TooManyRequestsException as e:
        return JSONResponse(
            content=e.serialize(), status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )
    except InternalServerException as e:
        return JSONResponse(
            content=e.serialize(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
