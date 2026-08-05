from typing import Protocol

from src.domain.models.search_snapshot import SearchSnapshot


class SearchRepository(Protocol):
    async def save(self, snapshot: SearchSnapshot) -> None:
        ...

    async def get(self, search_id: str) -> SearchSnapshot | None:
        ...

    async def list_recent(self, limit: int = 20) -> list[SearchSnapshot]:
        ...
