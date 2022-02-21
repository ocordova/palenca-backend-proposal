import os
from dataclasses import dataclass
from enum import Enum


class EnvName(Enum):
    STAGING = "staging"
    PRODUCTION = "production"
    DEVELOPMENT = "development"
    TESTING = "testing"
    SANDBOX = "sandbox"


def is_production(*, environment: str) -> bool:
    """Function that returns true if the environment passed as parameter is production
    :param str environment: The environment to compare
    :rtype: bool
    :return: If the environment is equal to production
    """
    return environment == EnvName.PRODUCTION.value


def is_staging(*, environment: str) -> bool:
    """Function that returns true if the environment passed as parameter is staging
    :param str environment: The environment to compare
    :rtype: bool
    :return: If the environment is equal to staging
    """
    return environment == EnvName.STAGING.value


def is_testing(*, environment: str) -> bool:
    """Function that returns true if the environment passed as parameter is testing
    :param str environment: The environment to compare
    :rtype: bool
    :return: If the environment is equal to testing
    """
    return environment == EnvName.TESTING.value


def is_development(*, environment: str) -> bool:
    """Function that returns true if the environment passed as parameter is development
    :param str environment: The environment to compare
    :rtype: bool
    :return: If the environment is equal to development
    """
    return environment == EnvName.DEVELOPMENT.value


def is_sandbox(*, environment: str) -> bool:
    """Function that returns true if the environment passed as parameter is sandbox
    :param str environment: The environment to compare
    :rtype: bool
    :return: If the environment is equal to sandbox
    """
    return environment == EnvName.SANDBOX.value


@dataclass
class Environment:

    ENVIRONMENT: EnvName
    SENTRY_URI: str
    POSTGRES_URI: str
    PORT: int


Env = Environment(
    ENVIRONMENT=EnvName(os.environ["ENVIRONMENT"]),
    SENTRY_URI=os.environ["SENTRY_URI"],
    POSTGRES_URI=os.environ["POSTGRES_URI"],
    PORT=int(os.environ["PORT"]),
)

TORTOISE_ORM = {
    "connections": {
        "default": "postgres://postgres:@host.docker.internal:5432/palenca_neue"
    },
    "apps": {
        "models": {
            "models": ["api.data.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
