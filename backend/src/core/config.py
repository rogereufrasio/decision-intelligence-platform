from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    app_name: str = (
        "Decision Intelligence Platform API"
    )

    app_version: str = "0.1.0"

    app_environment: str = (
        "development"
    )

    travel_provider: str = "mock"

    search_persistence_enabled: bool = False

    search_database_path: str = (
        "../data/searches.duckdb"
    )

    decision_persistence_enabled: bool = False

    decision_database_path: str = "../data/decisions.duckdb"

    amadeus_base_url: str = (
        "https://test.api.amadeus.com"
    )

    amadeus_client_id: str | None = None

    amadeus_client_secret: str | None = None

    duffel_base_url: str = (
        "https://api.duffel.com"
    )

    duffel_api_key: str | None = None

    http_timeout_seconds: int = 30


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
