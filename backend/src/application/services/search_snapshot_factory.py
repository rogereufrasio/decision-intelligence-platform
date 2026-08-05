from datetime import datetime, timezone
from uuid import uuid4

from src.domain.entities.decision import SortCriterion
from src.domain.models import SearchCriteria, SearchSnapshot, TravelResult
from src.shared.models import TravelSearchRequest


class SearchSnapshotFactory:
    SCHEMA_VERSION = "1.0"

    @classmethod
    def create(
        cls,
        request: TravelSearchRequest,
        result: TravelResult,
        sort_criterion: SortCriterion | None,
        correlation_id: str | None = None,
    ) -> SearchSnapshot:
        criteria = SearchCriteria.model_validate(
            {
                "origin": request.origin,
                "destination": request.destination,
                "departure_date": request.departure_date,
                "return_date": request.return_date,
                "adults": request.adults,
            }
        )

        return SearchSnapshot(
            search_id=str(uuid4()),
            criteria=criteria,
            created_at=datetime.now(timezone.utc),
            provider=result.provider,
            status=result.status,
            offers=result.offers,
            sort_criterion=sort_criterion,
            schema_version=cls.SCHEMA_VERSION,
            correlation_id=correlation_id,
            metadata=result.metadata or {},
            warnings=result.warnings,
        )
