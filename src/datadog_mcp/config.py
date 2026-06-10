"""Datadog settings loaded from environment variables.

Two keys identify the caller — an API key (organization) and an application key
(user, required for read / query endpoints) — plus ``site`` for the regional
endpoint (default US1, ``datadoghq.com``). All three use Datadog's ``DD_*``
names, so the official SDK reads the same variables. Read-only: no write toggle.
"""

from functools import lru_cache

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Auth(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DD_")

    api_key: SecretStr
    app_key: SecretStr
    site: str = "datadoghq.com"


@lru_cache
def get_auth() -> Auth:
    return Auth()  # type: ignore
