from hypothesis.strategies import builds, composite
from api.domain.entities import Client, User, AppLogin


@composite
def user_builder(draw, id=None):
    user = draw(strategy=builds(User))
    if id is not None:
        user.id = id
    return user


@composite
def client_builder(draw, id=None):
    client = draw(strategy=builds(Client))
    if id is not None:
        client.id = id
    return client


@composite
def app_login_builder(draw, user_id=None, client_id=None):
    app_login = draw(strategy=builds(AppLogin))
    if user_id is not None:
        app_login.user_id = user_id
    if client_id is not None:
        app_login.client_id = client_id

        
    return app_login

