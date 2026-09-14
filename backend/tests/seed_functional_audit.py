"""Deterministic persisted fixtures; never changes providers or HTTP responses."""
import asyncio
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import duckdb

from src.domain.models import Offer, PreferenceProfile, SearchCriteria, SearchSnapshot
from src.domain.models.decision_snapshot import DecisionSnapshot
from src.domain.services.recommendation_engine import RecommendationEngine
from src.domain.services.decision_explanation_engine import DecisionExplanationEngine
from src.infrastructure.persistence.duckdb_search_repository import DuckDBSearchRepository
from src.infrastructure.persistence.duckdb_decision_repository import DuckDBDecisionRepository


async def seed():
    root = Path(__file__).resolve().parents[2] / '.tmp'
    repository = DuckDBSearchRepository(root / 'e2e-searches.duckdb')
    now = datetime.now(timezone.utc)
    for index, (name, origin, price, currency) in enumerate([
        ('base', 'BSB', '500', 'BRL'), ('target', 'BSB', '450', 'BRL'),
        ('foreign', 'BSB', '90', 'USD'), ('empty', 'REC', None, 'BRL'),
        *[(f'page-{i}', 'SSA', '700', 'BRL') for i in range(22)],
    ]):
        offers = [] if price is None else [Offer(
            provider='mock', product_type='flight', price=price, currency=currency,
            attributes={'total_duration_minutes': 120, 'stops': 0},
        )]
        await repository.save(SearchSnapshot(
            search_id=f'audit-{name}', criteria=SearchCriteria(
                origin=origin, destination='GRU', departure_date='2027-01-10'),
            created_at=now - timedelta(minutes=30-index), provider='mock',
            status='success', offers=offers,
        ))
    offer = Offer(provider='mock', product_type='flight', price='450', currency='BRL')
    recommendations = RecommendationEngine().recommend([offer], PreferenceProfile.balanced())
    explanation = DecisionExplanationEngine().explain(tuple(recommendations), (), PreferenceProfile.balanced())
    await DuckDBDecisionRepository(root / 'e2e-decisions.duckdb').save(DecisionSnapshot(
        decision_id='audit-decision', search_id='audit-target', profile='balanced',
        accepted=tuple(recommendations), selected_offer=offer, explanation=explanation,
    ))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with duckdb.connect(':memory:') as connection:
            cursor = connection.execute('SELECT * FROM read_parquet(?)', [sys.argv[1]])
            print(json.dumps(dict(zip([c[0] for c in cursor.description], cursor.fetchone()))))
    else:
        asyncio.run(seed())
