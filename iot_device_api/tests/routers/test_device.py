from httpx import AsyncClient
from iot_device_api.models.device import Device, DeviceIn
import pytest
import json

async def create_device(device: DeviceIn, async_client: AsyncClient) -> dict:
    response = await async_client.post("/devices", json=device)
    return response.json()


@pytest.fixture()
async def created_device(async_client: AsyncClient):
    device = DeviceIn(name="test device", 
                      locationType="test location", 
                      category="test category",
                      status="test",
                      latitude=12354,
                      longitude=4134)
    
    device = device.model_dump_json()
    device = json.loads(device)

    return await create_device(device, async_client)


@pytest.mark.anyio
@pytest.mark.filterwarnings("ignore: The 'app'")
async def test_create_device(async_client: AsyncClient):
    """
    Test for creating a new device
    """
    device = DeviceIn(name="test device", 
                      locationType="test location", 
                      category="test category",
                      status="test",
                      latitude=12354,
                      longitude=4134)
    
    device = device.model_dump_json()
    device = json.loads(device)
    response = await async_client.post("/devices", json=device)
    
    assert response.status_code == 201
    assert {"id": 0, "name": "test device"}.items() <= response.json().items()



@pytest.mark.anyio
@pytest.mark.filterwarnings("ignore: The 'app'")
async def test_create_device_missing_data(async_client: AsyncClient):
    response = await async_client.post("/devices", json={})

    assert response.status_code != 201


@pytest.mark.anyio
@pytest.mark.filterwarnings("ignore: The 'app'")
async def test_get_all_devices(async_client: AsyncClient, created_device: dict):
    response = await async_client.get("/devices")

    assert response.status_code == 200
    assert response.json() == [created_device]