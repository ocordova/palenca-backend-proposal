from enum import Enum

from pydantic import BaseSettings, HttpUrl, PostgresDsn, AnyHttpUrl


class EnvName(Enum):
    production = "production"
    staging = "staging"
    development = "development"
    testing = "testing"
    sandbox = "sandbox"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvName
    SENTRY_URI: HttpUrl
    POSTGRES_URI: PostgresDsn
    PORT: int
    DOCUMENTATION_URI: HttpUrl
    MOCK_URI: AnyHttpUrl
    SIZE_POOL_AIOHTTP: int

    def is_production(self):
        return self.ENVIRONMENT.value == EnvName.development.value

    def is_staging(self):
        return self.ENVIRONMENT.value == EnvName.staging.value

    def is_development(self):
        return self.ENVIRONMENT.value == EnvName.development.value

    def is_testing(self):
        return self.ENVIRONMENT.value == EnvName.testing.value

    def is_sandbox(self):
        return self.ENVIRONMENT.value == EnvName.sandbox.value

    def is_development_or_sandbox(self):
        return self.ENVIRONMENT.value in [
            EnvName.development.value,
            EnvName.sandbox.value,
        ]


environment = EnvironmentSettings()

# For migrations
TORTOISE_ORM = {
    "connections": {"default": environment.POSTGRES_URI},
    "apps": {
        "models": {
            "models": ["api.data.postgres_models", "api.aerich.models"],
            "default_connection": "default",
        },
    },
}
