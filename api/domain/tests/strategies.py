from hypothesis.strategies import builds, composite
from api.domain.entities import Client, User


@composite
def user_builder(draw):
    user = draw(strategy=builds(User))
    return user

