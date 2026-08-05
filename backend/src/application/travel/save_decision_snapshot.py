from datetime import datetime, timezone
from uuid import uuid4

from src.application.ports import DecisionRepository
from src.domain.models import DecisionSnapshot, RecommendationEvaluation


class SaveDecisionSnapshotUseCase:
    def __init__(self, repository: DecisionRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        evaluation: RecommendationEvaluation,
        search_id: str | None = None,
        correlation_id: str | None = None,
    ) -> DecisionSnapshot:
        snapshot = DecisionSnapshot(
            decision_id=str(uuid4()), search_id=search_id,
            created_at=datetime.now(timezone.utc),
            profile=evaluation.explanation.profile,
            accepted=evaluation.accepted, rejected=evaluation.rejected,
            explanation=evaluation.explanation,
            selected_offer=evaluation.explanation.selected_offer,
            correlation_id=correlation_id,
        )
        await self.repository.save(snapshot)
        return snapshot
