import pytest

from unittest.mock import Mock, AsyncMock

from src.application.travel.search_orchestrator import SearchOrchestrator
from src.domain.models import Offer
from src.domain.models.travel_result import TravelResult
from src.shared.models import TravelSearchRequest


@pytest.mark.asyncio
async def test_search_orchestrator_delegates_and_returns_same_result():
    provider_response = TravelResult(
        provider="mock",
        status="success",
        message="",
        offers=[Offer(provider="mock", product_type="flight", price="100", currency="BRL")],
    )

    mock_strategy = Mock()
    mock_strategy.search = AsyncMock(return_value=provider_response)

    mock_engine = Mock()
    mock_engine.rank_offers = Mock(return_value=provider_response.offers)

    orchestrator = SearchOrchestrator(provider_strategy=mock_strategy, decision_engine=mock_engine)

    request = TravelSearchRequest(
        origin="GIG",
        destination="BRC",
        departure_date="2026-09-03",
        return_date="2026-09-07",
        adults=2,
    )

    response = await orchestrator.search(request)

    mock_strategy.search.assert_awaited_once_with(request)
    mock_engine.rank_offers.assert_called_once_with(provider_response.offers, None)
    assert response is provider_response
