from src.application.ports import SearchRepository
from src.domain.models import PriceIntelligence
from src.domain.services import PriceIntelligenceEngine


class AnalyzePriceHistoryUseCase:
    def __init__(
        self,
        repository: SearchRepository,
        engine: PriceIntelligenceEngine,
    ) -> None:
        self.repository = repository
        self.engine = engine

    async def execute(
        self,
        search_id: str,
        limit: int = 20,
    ) -> PriceIntelligence | None:
        if not 2 <= limit <= 100:
            raise ValueError("limit must be between 2 and 100")

        base_snapshot = await self.repository.get(search_id)
        if base_snapshot is None:
            return None

        recent_snapshots = await self.repository.list_recent(limit)
        comparable_snapshots = [
            base_snapshot,
            *[
                snapshot
                for snapshot in recent_snapshots
                if (
                    snapshot.search_id != base_snapshot.search_id
                    and snapshot.criteria == base_snapshot.criteria
                )
            ],
        ]
        return self.engine.analyze(comparable_snapshots)
