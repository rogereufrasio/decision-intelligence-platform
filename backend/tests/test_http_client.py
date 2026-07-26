import pytest

from src.infrastructure.http.client import HttpClient


@pytest.mark.asyncio
async def test_http_client_creation():

    client = HttpClient()

    assert client.client is not None

    await client.client.aclose()