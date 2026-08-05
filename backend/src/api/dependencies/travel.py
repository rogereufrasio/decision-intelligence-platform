from src.application.ports import AIAssistant
from src.application.travel.analyze_price_history import (
    AnalyzePriceHistoryUseCase,
)
from src.application.travel.compare_search_snapshots import (
    CompareSearchSnapshotsUseCase,
)
from src.application.travel.export_search_snapshot import (
    ExportSearchSnapshotUseCase,
)
from src.application.travel.get_decision_history import GetDecisionHistoryUseCase
from src.application.travel.get_search_history import (
    GetSearchHistoryUseCase,
)
from src.application.travel.get_search_snapshot import (
    GetSearchSnapshotUseCase,
)
from src.application.travel.recommend_travel_offers import (
    RecommendTravelOffersUseCase,
)
from src.application.travel.travel_service import TravelService
from src.infrastructure.container import Container


def get_ai_assistant() -> AIAssistant | None:
    return Container().get_ai_assistant()


def get_decision_history_use_case() -> GetDecisionHistoryUseCase | None:
    return Container().get_decision_history_use_case()


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


def get_compare_search_snapshots_use_case(
) -> CompareSearchSnapshotsUseCase | None:
    return Container().get_compare_search_snapshots_use_case()


def get_export_search_snapshot_use_case(
) -> ExportSearchSnapshotUseCase | None:
    return Container().get_export_search_snapshot_use_case()


def get_recommend_travel_offers_use_case() -> RecommendTravelOffersUseCase:
    return Container().get_recommend_travel_offers_use_case()


def get_analyze_price_history_use_case(
) -> AnalyzePriceHistoryUseCase | None:
    return Container().get_analyze_price_history_use_case()
