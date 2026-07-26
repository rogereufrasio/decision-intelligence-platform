from abc import ABC, abstractmethod

from src.domain.travel.models import TravelResult
from src.shared.models import TravelSearchRequest


class TravelProvider(ABC):

    @abstractmethod
    async def search(
        self,
        request: TravelSearchRequest,
    ) -> TravelResult:
        pass