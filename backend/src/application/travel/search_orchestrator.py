from __future__ import annotations

from src.shared.models import TravelSearchRequest, TravelSearchResponse


class SearchOrchestrator:

    def __init__(self, provider_strategy, decision_engine):
        # thin application service: only holds dependencies
        self.provider_strategy = provider_strategy
        self.decision_engine = decision_engine

    async def search(self, request: TravelSearchRequest) -> TravelSearchResponse:
        # Delegate entirely to provider strategy and decision engine without business logic
        response = await self.provider_strategy.search(request)

        # decision_engine.rank is expected to accept and return a TravelSearchResponse
        ranked = self.decision_engine.rank(response)

        return ranked
