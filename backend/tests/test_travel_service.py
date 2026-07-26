import pytest

from src.application.travel.travel_service import TravelService
from src.shared.models import TravelSearchRequest


@pytest.mark.asyncio
async def test_travel_service():

    service = TravelService()

    result = await service.search(
        TravelSearchRequest(
            origin="GIG",
            destination="BRC",
            departure_date="2026-09-03",
            return_date="2026-09-07",
            adults=2,
        )
    )

    assert result.provider == "mock"
    assert result.status == "success"