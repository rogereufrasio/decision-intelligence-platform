from src.infrastructure.http.client import HttpClient
from src.infrastructure.providers.provider_factory import ProviderFactory
from src.domain.travel.provider import TravelProvider
from src.infrastructure.providers.provider_strategy import ProviderStrategy
from src.domain.services.decision_engine import DecisionEngine
from src.application.travel.search_orchestrator import SearchOrchestrator


class Container:

    def __init__(self):

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
        strategy = ProviderStrategy()
        engine = DecisionEngine()

        # Adapter to expose the expected async search(request) signature
        class ProviderStrategyAdapter:
            def __init__(self, strategy):
                self._strategy = strategy

            async def search(self, request):
                from src.shared.models import TravelSearchResponse, TravelOfferResponse

                offers = await self._strategy.search(
                    request.origin,
                    request.destination,
                    request.departure_date,
                    request.return_date,
                    request.adults,
                )

                # Build a TravelSearchResponse from provider offers (in infrastructure)
                return TravelSearchResponse(
                    provider="strategy",
                    status="success",
                    message="",
                    offers=[TravelOfferResponse(price=o.price, currency=o.currency) for o in offers],
                )

        # Adapter to expose a rank(response) method expected by the orchestrator
        class DecisionEngineAdapter:
            def __init__(self, engine):
                self._engine = engine

            def rank(self, response):
                # For this block we keep orchestration only; no ranking logic applied here.
                # Return the response as-is to preserve existing behavior.
                return response

        adapter_strategy = ProviderStrategyAdapter(strategy)
        adapter_engine = DecisionEngineAdapter(engine)

        return SearchOrchestrator(provider_strategy=adapter_strategy, decision_engine=adapter_engine)

    async def close(self):

        await self.http_client.close()