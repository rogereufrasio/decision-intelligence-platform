from src.application.travel.travel_service import TravelService
from src.infrastructure.container import Container


def get_travel_service() -> TravelService:
    """
    Cria o serviço de viagem.
    """

    container = Container()
    return TravelService(
        orchestrator=container.get_search_orchestrator(),
    )
