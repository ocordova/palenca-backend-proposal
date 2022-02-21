from ...misc.entities import PhoneNumber
from ...domain.enums import CountryCode
from ...data.repositories import repo_get_user_by_id


async def indriver_create_user(
    *, user_id: str, phone_number: str, country: CountryCode
) -> None:
    print("####")
    user = await repo_get_user_by_id(user_id=user_id)
    print(user)

