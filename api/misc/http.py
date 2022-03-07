import asyncio
from multiprocessing.connection import Client
from sentry_sdk import capture_exception

from aiohttp import ClientSession, ClientTimeout, TCPConnector, ClientResponse
from typing import Optional, Any
from socket import AF_INET

from ..domain.exceptions import (
    InternalServerException,
    NotFoundException,
    UnauthorizedException,
    ForbiddenException,
    TooManyRequestsException,
)
from .config import environment


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

    def __handle_unknown_exceptions(exception: Exception):
        if environment.is_production_or_sandbox():
            capture_exception(e)
        raise InternalServerException()

    def __handle_client_errors(response: ClientResponse):
        status = response.status
        if status == 401:
            raise UnauthorizedException()
        if status == 403:
            raise ForbiddenException()
        if status == 404:
            raise NotFoundException()
        if status == 429:
            raise TooManyRequestsException()
        raise InternalServerException()

    async def __handle_success_response(cls, response: ClientResponse):
        try:
            json_result = await response.json()
        except Exception as e:
            cls.__handle_unknown_exceptions(exception=e)
        return json_result

    @classmethod
    async def post(
        cls, url: str, payload: Optional[dict] = None, headers: Optional[dict] = None,
    ) -> Any:
        client = cls.get_aiohttp_client()
        if headers is not None:
            client.headers = headers
        try:
            async with client.post(url, data=payload) as response:
                status = response.status
                if status > 210:
                    cls.__handle_client_errors(response)
                else:
                    json_result = cls.__handle_success_response
        except Exception as e:
            cls.__handle_unknown_exceptions(exception=e)

        return json_result
