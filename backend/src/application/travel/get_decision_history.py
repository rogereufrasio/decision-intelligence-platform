from src.application.ports import DecisionRepository
from src.domain.models import DecisionSnapshot


class GetDecisionHistoryUseCase:
    def __init__(self, repository: DecisionRepository) -> None:
        self.repository = repository

    async def execute(self, limit: int = 20) -> list[DecisionSnapshot]:
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")
        return await self.repository.list_recent(limit)
