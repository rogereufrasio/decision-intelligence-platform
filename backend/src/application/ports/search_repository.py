from typing import Protocol

from src.domain.models.search_snapshot import SearchSnapshot
from src.domain.models.search_criteria import SearchCriteria


class SearchRepository(Protocol):
    async def save(self, snapshot: SearchSnapshot) -> None:
        ...

    async def get(self, search_id: str) -> SearchSnapshot | None:
        ...

    async def list_recent(self, limit: int = 20) -> list[SearchSnapshot]:
        ...

    async def list_by_criteria(
        self,
        criteria: SearchCriteria,
        limit: int = 20,
    ) -> list[SearchSnapshot]:
        ...
