import pytest
from src.domain.travel.provider import TravelProvider
from src.infrastructure.providers.mock_provider import MockProvider
from src.infrastructure.providers.provider_registry import (
    ProviderNotFoundError,
    ProviderRegistry,
)


@pytest.fixture(autouse=True)
def cleanup_registry():
    """Garante isolamento limpando o registry antes e depois de cada teste."""
    ProviderRegistry.unregister_all()
    yield
    ProviderRegistry.unregister_all()


def test_register_and_get_provider_factory():
    def mock_factory(client=None) -> TravelProvider:
        return MockProvider()

    ProviderRegistry.register("mock", mock_factory)

    factory_fn = ProviderRegistry.get_factory("mock")
    provider_instance = factory_fn(None)

    assert isinstance(provider_instance, MockProvider)


def test_get_provider_case_insensitive():
    def mock_factory(client=None) -> TravelProvider:
        return MockProvider()

    ProviderRegistry.register("MockProvider", mock_factory)

    assert ProviderRegistry.get_factory("mockprovider") == mock_factory
    assert ProviderRegistry.get_factory("MOCKPROVIDER") == mock_factory


def test_get_unregistered_provider_raises_error():
    with pytest.raises(ProviderNotFoundError) as exc_info:
        ProviderRegistry.get_factory("non_existent")

    assert "Provider 'non_existent' não está registrado" in str(exc_info.value)


def test_list_available_providers():
    def dummy_factory(client=None) -> TravelProvider:
        return MockProvider()

    ProviderRegistry.register("mock", dummy_factory)
    ProviderRegistry.register("amadeus", dummy_factory)

    available = ProviderRegistry.list_available()
    assert len(available) == 2
    assert "mock" in available
    assert "amadeus" in available