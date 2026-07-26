import pytest

from src.application.travel.search_travel import SearchTravelUseCase
from src.shared.models import TravelSearchRequest


@pytest.mark.asyncio
async def test_search_use_case():

    use_case = SearchTravelUseCase()

    response = await use_case.execute(

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