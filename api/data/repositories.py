from .models import UserPostgres
from ..domain.entities import User
from ..domain.adapters import user_postgres_adapter


async def repo_get_user_by_id(*, user_id: str) -> User:
    """
    :raises: DoesNotExist
    """

    user = await UserPostgres.filter(id=user_id)

    return user_postgres_adapter(user=user)
