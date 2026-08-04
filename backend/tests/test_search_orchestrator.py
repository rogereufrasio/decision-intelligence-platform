import pytest

from unittest.mock import Mock, AsyncMock

from src.application.travel.search_orchestrator import SearchOrchestrator
from src.shared.models import TravelSearchRequest, TravelSearchResponse, TravelOfferResponse


@pytest.mark.asyncio
async def test_search_orchestrator_delegates_and_returns_same_response():

    # Prepare a response object returned by the provider strategy
    provider_response = TravelSearchResponse(
        provider="mock",
        status="success",
        message="",
        offers=[TravelOfferResponse(price="100", currency="BRL")],
    )

    # Mocks
    mock_strategy = Mock()
    mock_strategy.search = AsyncMock(return_value=provider_response)

    # Decision engine returns the same object (could be mutated in real implementations)
    ranked_response = provider_response
    mock_engine = Mock()
    mock_engine.rank = Mock(return_value=ranked_response)

    orchestrator = SearchOrchestrator(provider_strategy=mock_strategy, decision_engine=mock_engine)

    request = TravelSearchRequest(
        origin="GIG",
        destination="BRC",
        departure_date="2026-09-03",
        return_date="2026-09-07",
        adults=2,
    )

    # Execute
    response = await orchestrator.search(request)

    # Provider strategy should be called with the request object
    mock_strategy.search.assert_awaited_once_with(request)

    # Decision engine should be called with the provider response
    mock_engine.rank.assert_called_once_with(provider_response)

    # The orchestrator returns whatever the decision engine returned
    assert response is ranked_response
