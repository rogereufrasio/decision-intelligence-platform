import pytest

from src.infrastructure.container import Container


@pytest.mark.asyncio
async def test_container_close():

    container = Container()

    assert container.http_client is not None

    await container.close()