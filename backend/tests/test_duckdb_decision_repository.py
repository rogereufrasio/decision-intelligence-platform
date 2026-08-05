from datetime import datetime, timedelta, timezone
from decimal import Decimal
from pathlib import Path

import duckdb
import pytest
from pydantic import ValidationError

from src.domain.models import (
    DecisionExplanation,
    DecisionSnapshot,
    Offer,
    PreferenceProfile,
    Recommendation,
    RecommendationScore,
)
from src.infrastructure.persistence import DuckDBDecisionRepository


def create_snapshot(
    decision_id: str,
    created_at: datetime,
    *,
    price: str = "150.25",
) -> DecisionSnapshot:
    profile = PreferenceProfile.balanced()
    offer = Offer(
        provider="mock",
        product_type="flight",
        price=Decimal(price),
        currency="BRL",
    )
    recommendation = Recommendation(
        offer=offer,
        score=RecommendationScore(
            overall_score=Decimal("87.50"),
            price_score=Decimal("90"),
            duration_score=Decimal("85"),
            provider_score=Decimal("50"),
        ),
        rank=1,
        profile=profile,
        reasons=("Lowest price",),
    )
    explanation = DecisionExplanation(
        summary="Selected mock.",
        reasons=recommendation.reasons,
        rejected_count=0,
        profile=profile.name,
        selected_offer=offer,
        selected_provider=offer.provider,
        selected_price=offer.price,
        selected_currency=offer.currency,
    )
    return DecisionSnapshot(
        decision_id=decision_id,
        search_id="search-1",
        created_at=created_at,
        profile=profile.name,
        accepted=(recommendation,),
        explanation=explanation,
        selected_offer=offer,
        correlation_id="correlation-1",
    )


@pytest.mark.asyncio
async def test_creates_table_automatically(tmp_path: Path) -> None:
    path = tmp_path / "decisions.duckdb"
    repository = DuckDBDecisionRepository(path)

    assert await repository.list_recent() == []
    connection = duckdb.connect(str(path), read_only=True)
    try:
        assert ("decision_snapshots",) in connection.execute("SHOW TABLES").fetchall()
    finally:
        connection.close()


@pytest.mark.asyncio
async def test_save_get_and_round_trip_types(tmp_path: Path) -> None:
    repository = DuckDBDecisionRepository(tmp_path / "decisions.duckdb")
    snapshot = create_snapshot(
        "decision-1", datetime(2026, 8, 5, 12, tzinfo=timezone.utc)
    )

    await repository.save(snapshot)
    restored = await repository.get("decision-1")

    assert restored == snapshot
    assert restored is not None
    assert restored.created_at.utcoffset() == timedelta(0)
    assert restored.selected_offer is not None
    assert restored.selected_offer.price == Decimal("150.25")
    assert restored.profile is snapshot.profile


@pytest.mark.asyncio
async def test_upserts_by_decision_id(tmp_path: Path) -> None:
    repository = DuckDBDecisionRepository(tmp_path / "decisions.duckdb")
    created_at = datetime(2026, 8, 5, tzinfo=timezone.utc)
    await repository.save(create_snapshot("same", created_at, price="100"))
    await repository.save(create_snapshot("same", created_at, price="90"))

    restored = await repository.get("same")
    assert restored is not None
    assert restored.selected_offer is not None
    assert restored.selected_offer.price == Decimal("90")
    assert len(await repository.list_recent()) == 1


@pytest.mark.asyncio
async def test_list_recent_orders_descending_and_applies_limit(tmp_path: Path) -> None:
    repository = DuckDBDecisionRepository(tmp_path / "decisions.duckdb")
    base = datetime(2026, 8, 5, tzinfo=timezone.utc)
    for index in range(3):
        await repository.save(
            create_snapshot(f"decision-{index}", base + timedelta(hours=index))
        )

    recent = await repository.list_recent(limit=2)
    assert [item.decision_id for item in recent] == ["decision-2", "decision-1"]


@pytest.mark.asyncio
async def test_databases_are_isolated(tmp_path: Path) -> None:
    first = DuckDBDecisionRepository(tmp_path / "first.duckdb")
    second = DuckDBDecisionRepository(tmp_path / "second.duckdb")
    await first.save(
        create_snapshot("decision", datetime.now(timezone.utc))
    )

    assert await first.get("decision") is not None
    assert await second.get("decision") is None


def test_snapshot_is_immutable() -> None:
    snapshot = create_snapshot("decision", datetime.now(timezone.utc))

    with pytest.raises(ValidationError):
        snapshot.decision_id = "changed"
