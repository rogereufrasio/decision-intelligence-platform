import asyncio
import json
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import duckdb

from src.application.ports.search_repository import SearchRepository
from src.domain.models.search_snapshot import SearchSnapshot


class DuckDBSearchRepository(SearchRepository):
    _CREATE_TABLE_SQL = """
        CREATE TABLE IF NOT EXISTS search_snapshots (
            search_id VARCHAR PRIMARY KEY,
            criteria_json VARCHAR NOT NULL,
            created_at VARCHAR NOT NULL,
            provider VARCHAR NOT NULL,
            status VARCHAR NOT NULL,
            offers_json VARCHAR NOT NULL,
            sort_criterion VARCHAR,
            schema_version VARCHAR NOT NULL,
            correlation_id VARCHAR,
            metadata_json VARCHAR NOT NULL,
            warnings_json VARCHAR NOT NULL
        )
    """

    _SELECT_COLUMNS = """
        search_id,
        criteria_json,
        created_at,
        provider,
        status,
        offers_json,
        sort_criterion,
        schema_version,
        correlation_id,
        metadata_json,
        warnings_json
    """

    def __init__(self, database_path: str | Path) -> None:
        self._database_path = str(database_path)

    async def save(self, snapshot: SearchSnapshot) -> None:
        await asyncio.to_thread(self._save, snapshot)

    async def get(self, search_id: str) -> SearchSnapshot | None:
        return await asyncio.to_thread(self._get, search_id)

    async def list_recent(self, limit: int = 20) -> list[SearchSnapshot]:
        if limit < 1:
            return []
        return await asyncio.to_thread(self._list_recent, limit)

    def _save(self, snapshot: SearchSnapshot) -> None:
        payload = snapshot.model_dump(mode="json")
        values = (
            snapshot.search_id,
            self._to_json(payload["criteria"]),
            payload["created_at"],
            snapshot.provider,
            snapshot.status,
            self._to_json(payload["offers"]),
            payload["sort_criterion"],
            snapshot.schema_version,
            snapshot.correlation_id,
            self._to_json(payload["metadata"]),
            self._to_json(payload["warnings"]),
        )

        connection = self._connect()
        try:
            connection.execute(self._CREATE_TABLE_SQL)
            connection.execute(
                """
                INSERT INTO search_snapshots VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                ON CONFLICT (search_id) DO UPDATE SET
                    criteria_json = excluded.criteria_json,
                    created_at = excluded.created_at,
                    provider = excluded.provider,
                    status = excluded.status,
                    offers_json = excluded.offers_json,
                    sort_criterion = excluded.sort_criterion,
                    schema_version = excluded.schema_version,
                    correlation_id = excluded.correlation_id,
                    metadata_json = excluded.metadata_json,
                    warnings_json = excluded.warnings_json
                """,
                values,
            )
        finally:
            connection.close()

    def _get(self, search_id: str) -> SearchSnapshot | None:
        connection = self._connect()
        try:
            connection.execute(self._CREATE_TABLE_SQL)
            row = connection.execute(
                f"""
                SELECT {self._SELECT_COLUMNS}
                FROM search_snapshots
                WHERE search_id = ?
                """,
                [search_id],
            ).fetchone()
        finally:
            connection.close()

        return self._to_snapshot(row) if row is not None else None

    def _list_recent(self, limit: int) -> list[SearchSnapshot]:
        connection = self._connect()
        try:
            connection.execute(self._CREATE_TABLE_SQL)
            rows = connection.execute(
                f"""
                SELECT {self._SELECT_COLUMNS}
                FROM search_snapshots
                ORDER BY created_at DESC, search_id ASC
                LIMIT ?
                """,
                [limit],
            ).fetchall()
        finally:
            connection.close()

        return [self._to_snapshot(row) for row in rows]

    def _connect(self) -> duckdb.DuckDBPyConnection:
        return duckdb.connect(self._database_path)

    @staticmethod
    def _to_json(value: Any) -> str:
        return json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )

    @staticmethod
    def _to_snapshot(row: Sequence[Any]) -> SearchSnapshot:
        return SearchSnapshot.model_validate(
            {
                "search_id": row[0],
                "criteria": json.loads(row[1]),
                "created_at": row[2],
                "provider": row[3],
                "status": row[4],
                "offers": json.loads(row[5]),
                "sort_criterion": row[6],
                "schema_version": row[7],
                "correlation_id": row[8],
                "metadata": json.loads(row[9]),
                "warnings": json.loads(row[10]),
            }
        )
