"""
Configuration for our tests.
"""

import os
from typing import AsyncGenerator, Generator
import pytest

from fastapi.testclient import TestClient
from httpx import AsyncClient


os.environ["ENV_STATE"] = "test"

from iot_device_api.database import database
from iot_device_api.main import app


@pytest.fixture(scope="session")
def anyio_backend():
    """Only runs once for entire test session."""
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        yield ac