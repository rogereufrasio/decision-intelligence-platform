from src.application.travel.search_orchestrator import SearchOrchestrator
from src.core.config import get_settings
from src.infrastructure.container import Container
from src.shared.models import TravelSearchRequest


class TravelService:

    def __init__(self, orchestrator: SearchOrchestrator | None = None):
        if orchestrator is not None:
            self.orchestrator = orchestrator
            return

        settings = get_settings()
        container = Container()
        # Container is responsible for wiring ProviderStrategy and DecisionEngine into the orchestrator
        self.orchestrator = container.get_search_orchestrator()

    async def search(
        self,
        request: TravelSearchRequest,
    ):

        return await self.orchestrator.search(request)