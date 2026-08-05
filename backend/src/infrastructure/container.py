from src.infrastructure.http.client import HttpClient
from src.core.config import Settings, get_settings
from src.infrastructure.providers.provider_factory import ProviderFactory
from src.domain.travel.provider import TravelProvider
from src.infrastructure.providers.provider_strategy import ProviderStrategy
from src.domain.services.decision_engine import DecisionEngine
from src.application.travel.search_orchestrator import SearchOrchestrator


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
        )

    async def close(self):

        await self.http_client.close()
