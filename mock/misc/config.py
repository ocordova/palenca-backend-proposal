from pydantic import BaseSettings, HttpUrl


class EnvironmentSettings(BaseSettings):
    SENTRY_URI: HttpUrl
    PORT: int


environment = EnvironmentSettings()
