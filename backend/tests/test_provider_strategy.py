import pytest
from src.domain.models import Offer, TravelResult
from src.domain.travel.provider import TravelProvider
from src.infrastructure.providers.provider_strategy import ProviderStrategy
from src.infrastructure.providers.provider_registry import ProviderRegistry
from src.shared.models import TravelSearchRequest


@pytest.fixture(autouse=True)
def setup_test_providers():
    class DummyProvider1(TravelProvider):
        async def search(self, request: TravelSearchRequest):
            return TravelResult(
                provider="dummy1",
                status="success",
                message="OK",
                offers=[
                    Offer(
                        provider="dummy1",
                        product_type="flight",
                        price="100.0",
                        currency="BRL",
                    )
                ],
            )

    class DummyProvider2(TravelProvider):
        async def search(self, request: TravelSearchRequest):
            return TravelResult(
                provider="dummy2",
                status="success",
                message="OK",
                offers=[
                    Offer(
                        provider="dummy2",
                        product_type="flight",
                        price="200.0",
                        currency="BRL",
                    )
                ],
            )

    ProviderRegistry.register("dummy1", lambda client=None: DummyProvider1())
    ProviderRegistry.register("dummy2", lambda client=None: DummyProvider2())

    yield

    ProviderRegistry.unregister_all()


@pytest.mark.asyncio
async def test_strategy_executes_single_provider():
    request = TravelSearchRequest(
        origin="GIG",
        destination="GRU",
        departure_date="2026-10-01",
        return_date=None,
        adults=1,
    )

    strategy = ProviderStrategy(provider_names=["dummy1"])
    result = await strategy.search(request)

    assert len(result.offers) == 1
    assert str(result.offers[0].price) == "100.0"
    assert result.offers[0].currency == "BRL"


@pytest.mark.asyncio
async def test_strategy_executes_multiple_providers():
    request = TravelSearchRequest(
        origin="GIG",
        destination="GRU",
        departure_date="2026-10-01",
        return_date=None,
        adults=1,
    )

    strategy = ProviderStrategy(provider_names=["dummy1", "dummy2"])
    result = await strategy.search(request)

    assert len(result.offers) == 2
    prices_found = {str(offer.price) for offer in result.offers}
    assert prices_found == {"100.0", "200.0"}


@pytest.mark.asyncio
async def test_strategy_handles_provider_failure_gracefully():
    class FailingProvider(TravelProvider):
        async def search(self, request: TravelSearchRequest):
            raise RuntimeError("API Timeout")

    ProviderRegistry.register("failing", lambda client=None: FailingProvider())

    request = TravelSearchRequest(
        origin="GIG",
        destination="GRU",
        departure_date="2026-10-01",
        return_date=None,
        adults=1,
    )

    strategy = ProviderStrategy(provider_names=["dummy1", "failing"])
    result = await strategy.search(request)

    # Deve retornar os resultados do provider funcional mesmo com a falha do outro
    assert len(result.offers) == 1
    assert str(result.offers[0].price) == "100.0"
    assert result.offers[0].currency == "BRL"