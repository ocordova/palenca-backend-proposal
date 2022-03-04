from pydantic import BaseSettings, PostgresDsn, HttpUrl
from enum import Enum


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
