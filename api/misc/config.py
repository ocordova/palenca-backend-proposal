from enum import Enum

from pydantic import BaseSettings, HttpUrl, PostgresDsn


class EnvName(Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
    TESTING = "testing"
    SANDBOX = "sandbox"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvName
    SENTRY_URI: HttpUrl
    POSTGRES_URI: PostgresDsn
    PORT: int
    DOCUMENTATION_URI: HttpUrl
    SIZE_POOL_AIOHTTP: int

    def is_production(self):
        return self.ENVIRONMENT.value == EnvName.DEVELOPMENT.value

    def is_staging(self):
        return self.ENVIRONMENT.value == EnvName.STAGING.value

    def is_development(self):
        return self.ENVIRONMENT.value == EnvName.DEVELOPMENT.value

    def is_testing(self):
        return self.ENVIRONMENT.value == EnvName.TESTING.value

    def is_sandbox(self):
        return self.ENVIRONMENT.value == EnvName.SANDBOX.value


environment = EnvironmentSettings()

# For migrations
TORTOISE_ORM = {
    "connections": {"default": environment.POSTGRES_URI},
    "apps": {
        "models": {
            "models": ["api.data.postgres_models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
