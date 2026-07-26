from src.application.travel.travel_service import TravelService
from src.application.dependencies.travel_dependencies import (
    get_travel_provider,
)


def get_travel_service() -> TravelService:
    """
    Cria o serviço de viagem com suas dependências.
    """

    provider = get_travel_provider()

    return TravelService(
        provider=provider,
    )