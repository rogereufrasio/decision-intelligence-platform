from typing import Protocol

from src.domain.models.decision_snapshot import DecisionSnapshot


class DecisionRepository(Protocol):
    async def save(self, snapshot: DecisionSnapshot) -> None: ...

    async def get(self, decision_id: str) -> DecisionSnapshot | None: ...

    async def list_recent(self, limit: int = 20) -> list[DecisionSnapshot]: ...
