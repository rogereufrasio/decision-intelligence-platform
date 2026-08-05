from __future__ import annotations

from typing import Protocol

from src.domain.entities.decision import SortCriterion
from src.domain.models import TravelResult
from src.domain.services.decision_engine import DecisionEngine
from src.shared.models import TravelSearchRequest


class ProviderStrategy(Protocol):

    async def search(self, request: TravelSearchRequest) -> TravelResult:
        ...


class SearchOrchestrator:

    def __init__(
        self,
        provider_strategy: ProviderStrategy,
        decision_engine: DecisionEngine,
    ) -> None:
        self.provider_strategy = provider_strategy
        self.decision_engine = decision_engine

    async def search(
        self,
        request: TravelSearchRequest,
        criterion: SortCriterion | None = None,
    ) -> TravelResult:
        result = await self.provider_strategy.search(request)
        result.offers = self.decision_engine.rank_offers(
            result.offers,
            criterion,
        )
        return result
