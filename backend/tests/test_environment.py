from src.core.config import get_settings


def test_default_settings():

    settings = get_settings()

    assert (
        settings.app_name
        ==
        "Decision Intelligence Platform API"
    )

    assert (
        settings.travel_provider
        ==
        "mock"
    )

    assert (
        settings.http_timeout_seconds
        ==
        30
    )