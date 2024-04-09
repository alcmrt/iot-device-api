"""
Configuration for our tests.
"""

from typing import AsyncGenerator, Generator
import pytest

from fastapi.testclient import TestClient
from httpx import AsyncClient

from iot_device_api.main import app
from iot_device_api.routers.device import device_table


@pytest.fixture(scope="session")
def anyio_backend():
    """Only runs once for entire test session."""
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    device_table.clear()
    yield


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac