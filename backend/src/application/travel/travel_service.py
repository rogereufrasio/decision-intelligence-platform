from src.application.travel.search_orchestrator import SearchOrchestrator
from src.domain.entities.decision import SortCriterion
from src.domain.models import TravelResult
from src.shared.models import TravelSearchRequest


class TravelService:

    def __init__(self, orchestrator: SearchOrchestrator) -> None:
        self.orchestrator = orchestrator

    async def search(
        self,
        request: TravelSearchRequest,
        criterion: SortCriterion | None = None,
    ) -> TravelResult:
        return await self.orchestrator.search(request, criterion)
