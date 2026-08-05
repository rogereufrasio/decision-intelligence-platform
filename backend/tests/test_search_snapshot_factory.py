from datetime import date, timedelta
from decimal import Decimal
from uuid import UUID

from src.application.services.search_snapshot_factory import (
    SearchSnapshotFactory,
)
from src.domain.entities.decision import SortCriterion
from src.domain.models import Offer, TravelResult
from src.shared.models import TravelSearchRequest


def test_factory_creates_snapshot_from_ranked_result() -> None:
    request = TravelSearchRequest(
        origin="GIG",
        destination="GRU",
        departure_date="2026-09-03",
        return_date="2026-09-07",
        adults=2,
    )
    offer = Offer(
        provider="mock",
        product_type="flight",
        price=Decimal("150.25"),
        currency="BRL",
    )
    result = TravelResult(
        provider="mock",
        status="success",
        message="Offers retrieved",
        offers=[offer],
        metadata={"source": "test"},
        warnings=["partial result"],
    )

    snapshot = SearchSnapshotFactory.create(
        request=request,
        result=result,
        sort_criterion=SortCriterion.BEST_VALUE,
        correlation_id="correlation-1",
    )

    assert UUID(snapshot.search_id).version == 4
    assert snapshot.created_at.utcoffset() == timedelta(0)
    assert snapshot.criteria.origin == "GIG"
    assert snapshot.criteria.destination == "GRU"
    assert snapshot.criteria.departure_date == date(2026, 9, 3)
    assert snapshot.criteria.return_date == date(2026, 9, 7)
    assert snapshot.criteria.adults == 2
    assert snapshot.offers[0] is offer
    assert snapshot.sort_criterion is SortCriterion.BEST_VALUE
    assert snapshot.schema_version == "1.0"
    assert snapshot.correlation_id == "correlation-1"
    assert snapshot.metadata == {"source": "test"}
    assert snapshot.warnings == ["partial result"]
