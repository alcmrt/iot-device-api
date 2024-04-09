from datetime import datetime
from fastapi import APIRouter, HTTPException
from iot_device_api.models.device import Device, DeviceIn
from iot_device_api.database import device_table, database


router = APIRouter()
#device_table = []

"""
async def find_device(device_id: int):
    query = device_table.select().where(device_table.c.id == device_id)
    return await database.fetch_one(query)
"""


@router.post("/devices", response_model=Device, status_code=201)
async def create_device(device: DeviceIn):
    data = device.model_dump()
    data["createTime"] = datetime.now()
    data["updateTime"] = datetime.now()

    query = device_table.insert().values(data)
    last_record_id = await database.execute(query)

    new_device = {"id": last_record_id, **data}
    return new_device


@router.get("/devices", response_model=list[Device], status_code=200)
async def get_all_devices():
    query = device_table.select()
    return await database.fetch_all(query)



@router.get("/devices/{id}", response_model=Device, status_code=200)
async def get_device(id: int):
    query = device_table.select().where(device_table.c.id == id)
    device = await database.fetch_one(query)

    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")

    return device