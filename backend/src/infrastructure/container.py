from src.application.ports import SearchRepository
from src.application.travel.get_search_history import (
    GetSearchHistoryUseCase,
)
from src.application.travel.get_search_snapshot import (
    GetSearchSnapshotUseCase,
)
from src.application.travel.search_orchestrator import SearchOrchestrator
from src.core.config import Settings, get_settings
from src.domain.services.decision_engine import DecisionEngine
from src.domain.travel.provider import TravelProvider
from src.infrastructure.http.client import HttpClient
from src.infrastructure.persistence import DuckDBSearchRepository
from src.infrastructure.providers.provider_factory import ProviderFactory
from src.infrastructure.providers.provider_strategy import ProviderStrategy


class Container:

    def __init__(self, settings: Settings | None = None):

        self.settings = settings or get_settings()
        self.http_client = HttpClient()

    def get_travel_provider(
        self,
        provider_name: str,
    ) -> TravelProvider:

        return ProviderFactory.create(
            provider_name=provider_name,
            client=self.http_client,
        )

    def get_search_orchestrator(self) -> SearchOrchestrator:
        strategy = ProviderStrategy(
            provider_names=[self.settings.travel_provider],
        )
        engine = DecisionEngine()
        return SearchOrchestrator(
            provider_strategy=strategy,
            decision_engine=engine,
            search_repository=self.get_search_repository(),
        )

    def get_search_repository(self) -> SearchRepository | None:
        if not self.settings.search_persistence_enabled:
            return None

        return DuckDBSearchRepository(
            self.settings.search_database_path,
        )

    def get_search_history_use_case(
        self,
    ) -> GetSearchHistoryUseCase | None:
        repository = self.get_search_repository()
        if repository is None:
            return None
        return GetSearchHistoryUseCase(repository)

    def get_search_snapshot_use_case(
        self,
    ) -> GetSearchSnapshotUseCase | None:
        repository = self.get_search_repository()
        if repository is None:
            return None
        return GetSearchSnapshotUseCase(repository)

    async def close(self):

        await self.http_client.close()
