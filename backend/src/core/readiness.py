from dataclasses import dataclass
from os import R_OK, W_OK, access
from pathlib import Path

from src.core.config import Settings
from src.infrastructure.http.client import HttpClient


@dataclass(frozen=True)
class ReadinessCheck:
    name: str
    status: str
    message: str


@dataclass(frozen=True)
class ReadinessResult:
    ready: bool
    checks: tuple[ReadinessCheck, ...]


class ReadinessService:
    def __init__(self, settings: Settings, http_client: HttpClient) -> None:
        self._settings = settings
        self._http_client = http_client

    def evaluate(self) -> ReadinessResult:
        if not self._settings.readiness_enabled:
            return ReadinessResult(
                ready=False,
                checks=(ReadinessCheck(
                    name="readiness",
                    status="not_ready",
                    message="Readiness checks are disabled.",
                ),),
            )
        checks = [
            ReadinessCheck(
                name="configuration",
                status="ready",
                message="Application configuration is loaded.",
            ),
            self._http_client_check(),
            *self._persistence_checks(),
            self._optional_adapters_check(),
        ]
        if self._settings.external_dependency_check_enabled:
            checks.append(self._external_configuration_check())
        return ReadinessResult(
            ready=all(check.status == "ready" for check in checks),
            checks=tuple(checks),
        )

    def _http_client_check(self) -> ReadinessCheck:
        ready = not self._http_client.client.is_closed
        return ReadinessCheck(
            name="http_client",
            status="ready" if ready else "not_ready",
            message=(
                "HTTP client is available."
                if ready
                else "HTTP client is unavailable."
            ),
        )

    def _persistence_checks(self) -> list[ReadinessCheck]:
        configured_paths: list[tuple[str, str]] = []
        if self._settings.search_persistence_enabled:
            configured_paths.append(
                ("search_persistence", self._settings.search_database_path)
            )
        if self._settings.decision_persistence_enabled:
            configured_paths.append(
                ("decision_persistence", self._settings.decision_database_path)
            )
        return [
            self._directory_check(name, Path(path).parent)
            for name, path in configured_paths
        ]

    @staticmethod
    def _directory_check(name: str, directory: Path) -> ReadinessCheck:
        ready = (
            directory.exists()
            and directory.is_dir()
            and access(directory, R_OK | W_OK)
        )
        return ReadinessCheck(
            name=name,
            status="ready" if ready else "not_ready",
            message=(
                "Persistence directory is accessible."
                if ready
                else "Persistence directory is unavailable."
            ),
        )

    def _optional_adapters_check(self) -> ReadinessCheck:
        valid = (
            not self._settings.ai_assistant_enabled
            or self._settings.ai_assistant_provider == "template"
        )
        return ReadinessCheck(
            name="optional_adapters",
            status="ready" if valid else "not_ready",
            message=(
                "Optional adapters are correctly configured."
                if valid
                else "An enabled optional adapter is invalid."
            ),
        )

    def _external_configuration_check(self) -> ReadinessCheck:
        provider = self._settings.travel_provider
        valid = True
        if provider == "amadeus":
            valid = bool(
                self._settings.amadeus_client_id
                and self._settings.amadeus_client_secret
            )
        elif provider == "duffel":
            valid = bool(self._settings.duffel_api_key)
        elif provider != "mock":
            valid = False
        return ReadinessCheck(
            name="external_configuration",
            status="ready" if valid else "not_ready",
            message=(
                "External dependency configuration is valid."
                if valid
                else "External dependency configuration is incomplete."
            ),
        )
