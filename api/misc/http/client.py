import asyncio
from socket import AF_INET
from typing import Any, Optional

from aiohttp import ClientResponse, ClientSession, ClientTimeout, TCPConnector
from sentry_sdk import capture_exception

from api.misc.config import environment
from api.misc.http.exceptions import (
    ForbiddenHTTPException,
    InternalServerHTTPException,
    NotFoundHTTPException,
    TooManyRequestsHTTPException,
    UnauthorizedHTTPException,
)


class HTTPClient:
    sem: Optional[asyncio.Semaphore] = None
    aiohttp_client: Optional[ClientSession] = None

    @classmethod
    def get_aiohttp_client(cls) -> ClientSession:
        if cls.aiohttp_client is None:
            timeout = ClientTimeout(total=2)
            connector = TCPConnector(
                family=AF_INET, limit_per_host=environment.SIZE_POOL_AIOHTTP
            )
            cls.aiohttp_client = ClientSession(timeout=timeout, connector=connector)

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    def handle_unknown_exceptions(cls, exception: Exception):
        if environment.is_production():
            capture_exception(exception)
        raise InternalServerHTTPException()

    @classmethod
    def handle_client_errors(cls, response: ClientResponse):
        status = response.status
        if status == 401:
            raise UnauthorizedHTTPException()
        if status == 403:
            raise ForbiddenHTTPException()
        if status == 404:
            raise NotFoundHTTPException()
        if status == 429:
            raise TooManyRequestsHTTPException()
        raise InternalServerHTTPException()

    @classmethod
    async def handle_success_response(cls, response: ClientResponse):
        try:
            json_result = await response.json()
        except Exception as e:
            cls.handle_unknown_exceptions(exception=e)
        return json_result

    @classmethod
    async def post(
        cls,
        url: str,
        body: dict = None,
        headers: Optional[dict] = None,
    ) -> Any:
        client = cls.get_aiohttp_client()

        try:
            async with client.post(url, json=body, headers=headers) as response:
                status = response.status
                if status > 210:
                    cls.handle_client_errors(response=response)
                else:
                    json_result = await cls.handle_success_response(response=response)
        except Exception as e:
            cls.handle_unknown_exceptions(exception=e)
        return json_result
