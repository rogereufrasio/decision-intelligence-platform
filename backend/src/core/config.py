from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = "Decision Intelligence Platform API"
    app_version: str = "0.1.0"
    app_environment: str = "development"

    travel_provider: str = "mock"

    amadeus_base_url: str = "https://test.api.amadeus.com"
    amadeus_client_id: str | None = None
    amadeus_client_secret: str | None = None

    http_timeout_seconds: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()