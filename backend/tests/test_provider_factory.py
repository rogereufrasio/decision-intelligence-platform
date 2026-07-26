from src.infrastructure.providers.amadeus_provider import AmadeusProvider
from src.infrastructure.providers.mock_provider import MockTravelProvider
from src.infrastructure.providers.provider_factory import ProviderFactory


def test_create_mock_provider():

    provider = ProviderFactory.create(
        "mock"
    )

    assert isinstance(
        provider,
        MockTravelProvider,
    )


def test_create_amadeus_provider():

    provider = ProviderFactory.create(
        "amadeus"
    )

    assert isinstance(
        provider,
        AmadeusProvider,
    )


def test_create_invalid_provider():

    try:
        ProviderFactory.create(
            "invalid"
        )

        assert False

    except ValueError as exception:

        assert str(exception) == (
            "Unsupported travel provider: invalid"
        )