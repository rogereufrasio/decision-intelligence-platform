from __future__ import annotations

from typing import Protocol

from src.application.ports import SearchRepository
from src.application.services.search_snapshot_factory import (
    SearchSnapshotFactory,
)
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
        search_repository: SearchRepository | None = None,
    ) -> None:
        self.provider_strategy = provider_strategy
        self.decision_engine = decision_engine
        self.search_repository = search_repository

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

        if self.search_repository is not None:
            snapshot = SearchSnapshotFactory.create(
                request=request,
                result=result,
                sort_criterion=criterion,
            )
            await self.search_repository.save(snapshot)

        return result
