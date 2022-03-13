from fastapi import Depends, Request, status
from fastapi.responses import JSONResponse

from mock.pedidosya.domain.exceptions import UnauthorizedException


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except UnauthorizedException as e:
        return JSONResponse(
            content=e.serialize(), status_code=status.HTTP_401_UNAUTHORIZED
        )
