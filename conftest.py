import os

import pytest
from tortoise.contrib.test import finalizer, initializer


@pytest.fixture(autouse=True)
def db():
    db_url = os.environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    initializer(["api.data.postgres_models"], db_url=db_url)
    yield
    finalizer()
