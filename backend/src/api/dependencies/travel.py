from src.application.travel.get_search_history import (
    GetSearchHistoryUseCase,
)
from src.application.travel.get_search_snapshot import (
    GetSearchSnapshotUseCase,
)
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


def get_search_history_use_case() -> GetSearchHistoryUseCase | None:
    return Container().get_search_history_use_case()


def get_search_snapshot_use_case() -> GetSearchSnapshotUseCase | None:
    return Container().get_search_snapshot_use_case()
