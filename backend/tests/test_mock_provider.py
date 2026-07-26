import pytest

from src.infrastructure.providers.mock_provider import MockTravelProvider
from src.shared.models import TravelSearchRequest


@pytest.mark.asyncio
async def test_mock_provider():

    provider = MockTravelProvider()

    response = await provider.search(

        TravelSearchRequest(
            origin="GIG",
            destination="BRC",
            departure_date="2026-09-03",
            return_date="2026-09-07",
            adults=2,
        )

    )

    assert response.provider == "mock"

    assert response.status == "success"