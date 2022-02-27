from ..misc.entities import PhoneNumber
from ..domain.entities import Client, User
from ..domain.enums import CountryCode
from ..data.repositories import repo_get_user_client_and_user, repo_create_user
from ..misc.utils import create_timestamp
from ..domain.exceptions import UnableToCreateUser


async def create_or_get_user(client: Client, user_id: str = None) -> User:

    user = None

    if not user_id:
        user_id = create_timestamp()

    user = await repo_get_user_client_and_user(client_id=client.id, user_id=user_id)

    if not user:
        user = await repo_create_user(client=client, user_id=user_id)

    if not user:
        UnableToCreateUser()

    return user


async def indriver_create_user(
    *,
    auth_client: Client,
    user_id: str,
    phone_number: str,
    country: CountryCode,
    source: str
) -> User:

    user = await create_or_get_user(client=auth_client, user_id=user_id)

    return user
