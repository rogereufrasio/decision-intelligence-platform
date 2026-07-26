from src.infrastructure.providers.base_provider import BaseProvider


def test_base_provider():

    provider = BaseProvider(
        base_url="https://example.com"
    )

    assert provider.base_url == "https://example.com"