from typing import Optional
from .models import ClientPostgres, UserPostgres
from ..domain.entities import Client, User
from ..domain.adapters import client_postgres_adapter, user_postgres_adapter
from ..domain.exceptions import NotFoundException


async def repo_get_client_by_api_key(*, api_key: str) -> Client:
    """
    :raises: NotFoundException
    """

    client = await ClientPostgres.get_or_none(api_key=api_key)

    if client is None:
        raise NotFoundException("Client not found")

    return client_postgres_adapter(client=client)


async def repo_get_user_client_and_user(
    *, client_id: int, user_id: str
) -> Optional[User]:
    user = await UserPostgres.get_or_none(
        client_id=client_id, user_id=user_id
    ).select_related("client")

    if user is None:
        return None

    return user_postgres_adapter(user=user)


async def repo_create_user(*, client: Client, user_id: str) -> User:
    user = await UserPostgres.create(user_id=user_id, client_id=client.id)

    return user_postgres_adapter(user=user)
