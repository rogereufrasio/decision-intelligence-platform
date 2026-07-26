from src.domain.travel.provider import TravelProvider
from src.core.config import get_settings
from src.infrastructure.providers.provider_factory import ProviderFactory


def get_travel_provider() -> TravelProvider:
    """
    Cria o provider de viagem configurado para a aplicação.
    """

    settings = get_settings()

    return ProviderFactory.create(
        settings.travel_provider
    )