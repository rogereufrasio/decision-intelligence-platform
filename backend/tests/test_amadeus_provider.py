import pytest

from src.infrastructure.providers.amadeus_provider import AmadeusProvider


@pytest.mark.asyncio
async def test_amadeus_provider_requires_credentials():

    provider = AmadeusProvider()

    with pytest.raises(ValueError):
        await provider.authenticate()