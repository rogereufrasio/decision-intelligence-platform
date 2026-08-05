from unittest.mock import AsyncMock, Mock

import pytest

from src.application.travel.search_orchestrator import SearchOrchestrator
from src.domain.entities.decision import SortCriterion
from src.domain.models import Offer, SearchSnapshot
from src.domain.models.travel_result import TravelResult
from src.shared.models import TravelSearchRequest


class FakeSearchRepository:
    def __init__(self) -> None:
        self.saved_snapshots: list[SearchSnapshot] = []

    async def save(self, snapshot: SearchSnapshot) -> None:
        self.saved_snapshots.append(snapshot)

    async def get(self, search_id: str) -> SearchSnapshot | None:
        return next(
            (
                snapshot
                for snapshot in self.saved_snapshots
                if snapshot.search_id == search_id
            ),
            None,
        )

    async def list_recent(self, limit: int = 20) -> list[SearchSnapshot]:
        return self.saved_snapshots[-limit:]


class FailingSearchRepository(FakeSearchRepository):
    async def save(self, snapshot: SearchSnapshot) -> None:
        raise RuntimeError("Persistence unavailable")


@pytest.mark.asyncio
async def test_search_orchestrator_delegates_and_returns_same_result(
) -> None:
    provider_response = TravelResult(
        provider="mock",
        status="success",
        message="",
        offers=[
            Offer(
                provider="mock",
                product_type="flight",
                price="100",
                currency="BRL",
            )
        ],
    )

    mock_strategy = Mock()
    mock_strategy.search = AsyncMock(return_value=provider_response)

    mock_engine = Mock()
    mock_engine.rank_offers = Mock(return_value=provider_response.offers)

    orchestrator = SearchOrchestrator(
        provider_strategy=mock_strategy,
        decision_engine=mock_engine,
    )

    request = TravelSearchRequest(
        origin="GIG",
        destination="BRC",
        departure_date="2026-09-03",
        return_date="2026-09-07",
        adults=2,
    )

    response = await orchestrator.search(request)

    mock_strategy.search.assert_awaited_once_with(request)
    mock_engine.rank_offers.assert_called_once_with(
        provider_response.offers,
        None,
    )
    assert response is provider_response


@pytest.mark.asyncio
async def test_search_orchestrator_persists_ranked_snapshot() -> None:
    original_offer = Offer(
        provider="mock",
        product_type="flight",
        price="100",
        currency="BRL",
    )
    ranked_offer = Offer(
        provider="mock",
        product_type="flight",
        price="90",
        currency="BRL",
    )
    provider_response = TravelResult(
        provider="mock",
        status="success",
        message="",
        offers=[original_offer],
    )

    mock_strategy = Mock()
    mock_strategy.search = AsyncMock(return_value=provider_response)
    mock_engine = Mock()
    mock_engine.rank_offers = Mock(return_value=[ranked_offer])
    repository = FakeSearchRepository()
    orchestrator = SearchOrchestrator(
        provider_strategy=mock_strategy,
        decision_engine=mock_engine,
        search_repository=repository,
    )
    request = TravelSearchRequest(
        origin="GIG",
        destination="BRC",
        departure_date="2026-09-03",
        return_date="2026-09-07",
        adults=2,
    )

    response = await orchestrator.search(request, SortCriterion.CHEAPEST)

    assert len(repository.saved_snapshots) == 1
    snapshot = repository.saved_snapshots[0]
    assert isinstance(snapshot, SearchSnapshot)
    assert snapshot.criteria.origin == request.origin
    assert snapshot.criteria.destination == request.destination
    assert snapshot.offers == [ranked_offer]
    assert snapshot.sort_criterion is SortCriterion.CHEAPEST
    assert response is provider_response
    assert response.offers == [ranked_offer]


@pytest.mark.asyncio
async def test_search_orchestrator_propagates_repository_error() -> None:
    provider_response = TravelResult(
        provider="mock",
        status="success",
        message="",
        offers=[],
    )
    mock_strategy = Mock()
    mock_strategy.search = AsyncMock(return_value=provider_response)
    mock_engine = Mock()
    mock_engine.rank_offers = Mock(return_value=[])
    repository = FailingSearchRepository()
    orchestrator = SearchOrchestrator(
        provider_strategy=mock_strategy,
        decision_engine=mock_engine,
        search_repository=repository,
    )
    request = TravelSearchRequest(
        origin="GIG",
        destination="BRC",
        departure_date="2026-09-03",
        adults=1,
    )

    with pytest.raises(RuntimeError, match="Persistence unavailable"):
        await orchestrator.search(request)
