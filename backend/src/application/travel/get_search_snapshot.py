from src.application.ports import SearchRepository
from src.domain.models import SearchSnapshot


class GetSearchSnapshotUseCase:
    def __init__(self, repository: SearchRepository) -> None:
        self.repository = repository

    async def execute(self, search_id: str) -> SearchSnapshot | None:
        return await self.repository.get(search_id)
