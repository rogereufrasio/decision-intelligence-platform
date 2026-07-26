import pytest

from src.shared.provider_exceptions import ProviderException


def test_provider_exception_message():

    with pytest.raises(
        ProviderException,
        match="amadeus: timeout",
    ):

        raise ProviderException(
            "amadeus",
            "timeout",
        )