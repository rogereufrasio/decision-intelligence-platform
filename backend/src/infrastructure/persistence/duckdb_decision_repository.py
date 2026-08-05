import asyncio
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import duckdb

from src.application.ports.decision_repository import DecisionRepository
from src.domain.models.decision_snapshot import DecisionSnapshot


class DuckDBDecisionRepository(DecisionRepository):
    _CREATE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS decision_snapshots (
            decision_id VARCHAR PRIMARY KEY,
            search_id VARCHAR,
            created_at VARCHAR NOT NULL,
            profile VARCHAR NOT NULL,
            accepted_json VARCHAR NOT NULL,
            rejected_json VARCHAR NOT NULL,
            explanation_json VARCHAR NOT NULL,
            selected_offer_json VARCHAR,
            schema_version VARCHAR NOT NULL,
            correlation_id VARCHAR
        )
    """
    _COLUMNS = """decision_id, search_id, created_at, profile,
        accepted_json, rejected_json, explanation_json, selected_offer_json,
        schema_version, correlation_id"""

    def __init__(self, database_path: str | Path) -> None:
        self._database_path = str(database_path)

    async def save(self, snapshot: DecisionSnapshot) -> None:
        await asyncio.to_thread(self._save, snapshot)

    async def get(self, decision_id: str) -> DecisionSnapshot | None:
        return await asyncio.to_thread(self._get, decision_id)

    async def list_recent(self, limit: int = 20) -> list[DecisionSnapshot]:
        if limit < 1:
            return []
        return await asyncio.to_thread(self._list_recent, limit)

    def _connect(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(self._database_path)

    def _save(self, snapshot: DecisionSnapshot) -> None:
        payload = snapshot.model_dump(mode="json")
        selected = payload["selected_offer"]
        values = (
            snapshot.decision_id, snapshot.search_id, payload["created_at"],
            payload["profile"], self._json(payload["accepted"]),
            self._json(payload["rejected"]), self._json(payload["explanation"]),
            self._json(selected) if selected is not None else None,
            snapshot.schema_version, snapshot.correlation_id,
        )
        connection = self._connect()
        try:
            connection.execute(self._CREATE_TABLE_SQL)
            connection.execute(
                """INSERT INTO decision_snapshots VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT (decision_id) DO UPDATE SET
                    search_id=excluded.search_id, created_at=excluded.created_at,
                    profile=excluded.profile, accepted_json=excluded.accepted_json,
                    rejected_json=excluded.rejected_json,
                    explanation_json=excluded.explanation_json,
                    selected_offer_json=excluded.selected_offer_json,
                    schema_version=excluded.schema_version,
                    correlation_id=excluded.correlation_id""",
                values,
            )
        finally:
            connection.close()

    def _get(self, decision_id: str) -> DecisionSnapshot | None:
        connection = self._connect()
        try:
            connection.execute(self._CREATE_TABLE_SQL)
            row = connection.execute(
                f"SELECT {self._COLUMNS} FROM decision_snapshots WHERE decision_id = ?",
                [decision_id],
            ).fetchone()
        finally:
            connection.close()
        return self._snapshot(row) if row is not None else None

    def _list_recent(self, limit: int) -> list[DecisionSnapshot]:
        connection = self._connect()
        try:
            connection.execute(self._CREATE_TABLE_SQL)
            rows = connection.execute(
                f"SELECT {self._COLUMNS} FROM decision_snapshots "
                "ORDER BY created_at DESC, decision_id ASC LIMIT ?", [limit]
            ).fetchall()
        finally:
            connection.close()
        return [self._snapshot(row) for row in rows]

    @staticmethod
    def _json(value: Any) -> str:
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)

    @staticmethod
    def _snapshot(row: Sequence[Any]) -> DecisionSnapshot:
        return DecisionSnapshot.model_validate({
            "decision_id": row[0], "search_id": row[1], "created_at": row[2],
            "profile": row[3], "accepted": json.loads(row[4]),
            "rejected": json.loads(row[5]), "explanation": json.loads(row[6]),
            "selected_offer": json.loads(row[7]) if row[7] else None,
            "schema_version": row[8], "correlation_id": row[9],
        })
