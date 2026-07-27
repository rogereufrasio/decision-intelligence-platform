import pytest

from src.infrastructure.providers.amadeus_provider import AmadeusProvider
from src.infrastructure.http.client import HttpClient

@pytest.mark.asyncio
async def test_amadeus_provider_requires_credentials(
    monkeypatch,
):

    monkeypatch.delenv(
        "AMADEUS_CLIENT_ID",
        raising=False,
    )

    monkeypatch.delenv(
        "AMADEUS_CLIENT_SECRET",
        raising=False,
    )

    from src.core.config import get_settings

    get_settings.cache_clear()


    provider = AmadeusProvider(
        client=HttpClient()
    )


    with pytest.raises(
        ValueError,
        match="Amadeus credentials are not configured",
    ):
        await provider.authenticate()