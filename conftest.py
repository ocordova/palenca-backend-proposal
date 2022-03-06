import os

import pytest
from tortoise.contrib.test import finalizer, initializer

# def pytest_generate_tests(metafunc):
#     from api.misc.env import Env, EnvName

#     Env.ENVIRONMENT = EnvName.TESTING


# @pytest.fixture(autouse=True)
# def set_tortoise():
#     db_url = "sqlite://:memory:"
#     initializer(["api.data.models"], db_url=db_url)
#     finalizer()


# def pytest_runtest_setup():


@pytest.fixture(autouse=True)
def db(request):
    db_url = os.environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    initializer(["api.data.models"], db_url=db_url)
    yield
    finalizer()
