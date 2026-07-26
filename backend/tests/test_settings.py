from src.core.config import get_settings


def test_http_timeout_default():

    settings = get_settings()

    assert settings.http_timeout_seconds == 30