import pytest

from src.application.travel.search_travel_use_case import SearchTravelUseCase
from src.infrastructure.providers.mock_provider import MockTravelProvider
from src.shared.models import TravelSearchRequest


@pytest.mark.asyncio
async def test_search_use_case():

    provider = MockTravelProvider()

    use_case = SearchTravelUseCase(provider)

    request = TravelSearchRequest(
        origin="GIG",
        destination="BRC",
        departure_date="2026-09-03",
        return_date="2026-09-07",
        adults=2,
    )

    result = await use_case.execute(request)

    assert result.provider == "mock"