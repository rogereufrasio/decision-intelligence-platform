from src.infrastructure.providers.base_provider import BaseProvider
from src.infrastructure.http.client import HttpClient


def test_base_provider():

    provider = BaseProvider(
        client=HttpClient(),
        base_url="https://example.com",
    )

    assert provider.base_url == "https://example.com"