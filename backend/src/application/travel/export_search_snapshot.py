import asyncio
import json
import re
from pathlib import Path
from typing import Any

import duckdb

from src.application.ports import SearchRepository
from src.domain.models import SearchSnapshot


class ExportSearchSnapshotUseCase:
    def __init__(
        self,
        repository: SearchRepository,
        export_directory: str | Path,
    ) -> None:
        self.repository = repository
        self.export_directory = Path(export_directory)

    async def execute(self, search_id: str) -> Path | None:
        snapshot = await self.repository.get(search_id)
        if snapshot is None:
            return None

        return await asyncio.to_thread(self._export, snapshot)

    def _export(self, snapshot: SearchSnapshot) -> Path:
        self.export_directory.mkdir(parents=True, exist_ok=True)
        output_path = self.export_directory / self._file_name(
            snapshot.search_id
        )
        payload = snapshot.model_dump(mode="json")

        connection = duckdb.connect(":memory:")
        try:
            connection.execute(
                """
                CREATE TABLE snapshot_export (
                    search_id VARCHAR,
                    criteria_json VARCHAR,
                    created_at VARCHAR,
                    provider VARCHAR,
                    status VARCHAR,
                    offers_json VARCHAR,
                    sort_criterion VARCHAR,
                    schema_version VARCHAR,
                    correlation_id VARCHAR,
                    metadata_json VARCHAR,
                    warnings_json VARCHAR
                )
                """
            )
            connection.execute(
                """
                INSERT INTO snapshot_export VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
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
                ),
            )
            escaped_path = output_path.as_posix().replace("'", "''")
            connection.execute(
                f"""
                COPY snapshot_export
                TO '{escaped_path}'
                (FORMAT PARQUET)
                """
            )
        finally:
            connection.close()

        return output_path

    @staticmethod
    def _file_name(search_id: str) -> str:
        safe_search_id = re.sub(r"[^A-Za-z0-9._-]", "_", search_id)
        return f"search_{safe_search_id}.parquet"

    @staticmethod
    def _to_json(value: Any) -> str:
        return json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
