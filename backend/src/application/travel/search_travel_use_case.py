from src.domain.travel.provider import TravelProvider
from src.domain.travel.models import TravelResult
from src.domain.entities.decision import SortCriterion
from src.domain.services.decision_engine import DecisionEngine
from src.shared.models import TravelSearchRequest


class SearchTravelUseCase:

    def __init__(self, provider: TravelProvider):
        self.provider = provider

    async def execute(
        self,
        request: TravelSearchRequest,
        criterion: SortCriterion | None = None,
    ) -> TravelResult:
        result = await self.provider.search(request)

        if criterion is None:
            return result

        ranked_offers = DecisionEngine.rank_offers(
            result.offers,
            criterion,
        )

        return TravelResult(
            provider=result.provider,
            status=result.status,
            message=result.message,
            offers=ranked_offers,
        )