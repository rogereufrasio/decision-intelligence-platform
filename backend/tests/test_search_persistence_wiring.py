from pathlib import Path

import pytest

from src.core.config import Settings
from src.infrastructure.container import Container


@pytest.mark.asyncio
async def test_container_does_not_create_database_when_disabled(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "searches.duckdb"
    settings = Settings(
        search_persistence_enabled=False,
        search_database_path=str(database_path),
    )
    container = Container(settings=settings)

    try:
        orchestrator = container.get_search_orchestrator()

        assert orchestrator.search_repository is None
        assert not database_path.exists()
    finally:
        await container.close()
