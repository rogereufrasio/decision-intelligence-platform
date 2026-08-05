from src.application.ports import SearchRepository
from src.domain.models import SearchSnapshot


class GetSearchHistoryUseCase:
    def __init__(self, repository: SearchRepository) -> None:
        self.repository = repository

    async def execute(self, limit: int = 20) -> list[SearchSnapshot]:
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100")

        return await self.repository.list_recent(limit)
