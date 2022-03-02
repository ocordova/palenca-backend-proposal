from ..data.models import ClientPostgres, UserPostgres
from .entities import Client, UserExtraData, User
from .enums import Platform


def client_postgres_adapter(*, client: ClientPostgres) -> Client:
    return Client(
        id=client.id,
        email=client.email,
        api_key=client.api_key,
        company_name=client.company_name,
        client_id=client.client_id,
        logo_url=client.logo_name,
        platforms=list(map(lambda pt: Platform(pt), client.list_apps)),
        webhook_url=client.webhook_url,
        created_at=client.created_at,
        updated_at=client.updated_at,
    )


def user_postgres_adapter(*, user: UserPostgres) -> User:
    client_extra_data = None
    if user.extra_data:
        client_extra_data = UserExtraData(purpose=user.extra_data.get("purpose", None))
    return User(
        id=user.id,
        user_id=user.user_id,
        client=client_postgres_adapter(client=user.client),
        created_at=user.created_at,
        updated_at=user.updated_at,
        extra_data=client_extra_data,
    )
