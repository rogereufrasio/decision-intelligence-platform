import httpx
import pytest

from src.infrastructure.http.client import HttpClient
from src.infrastructure.http.exceptions import HttpClientException


@pytest.mark.asyncio
async def test_http_client_creation():

    client = HttpClient()

    assert client.client is not None

    await client.close()


@pytest.mark.asyncio
async def test_http_client_retries_before_success(monkeypatch):

    client = HttpClient()

    calls = 0

    class FakeResponse:

        status_code = 200

        def raise_for_status(self):
            return None

    async def fake_get(*args, **kwargs):

        nonlocal calls

        calls += 1

        if calls < 3:
            raise httpx.ConnectError(
                "temporary error"
            )

        return FakeResponse()

    monkeypatch.setattr(
        client.client,
        "get",
        fake_get,
    )

    response = await client.get(
        "https://example.com"
    )

    assert response is not None
    assert calls == 3

    await client.close()


@pytest.mark.asyncio
async def test_http_client_raises_after_max_retries(monkeypatch):

    client = HttpClient()

    async def fake_get(*args, **kwargs):

        raise httpx.ConnectError(
            "network unavailable"
        )

    monkeypatch.setattr(
        client.client,
        "get",
        fake_get,
    )

    with pytest.raises(
        HttpClientException,
    ):

        await client.get(
            "https://example.com"
        )

    await client.close()