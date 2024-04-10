import logging

from datetime import datetime
from fastapi import APIRouter, HTTPException
from iot_device_api.models.device import Device, DeviceIn
from iot_device_api.database import device_table, database


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/devices", response_model=Device, status_code=201)
async def create_device(device: DeviceIn):
    logger.info("Creating device")
    
    data = device.model_dump()
    data["createTime"] = datetime.now()
    data["updateTime"] = datetime.now()

    query = device_table.insert().values(data)
    logger.debug(query)
    
    last_record_id = await database.execute(query)
    new_device = {"id": last_record_id, **data}
    return new_device


@router.get("/devices", response_model=list[Device], status_code=200)
async def get_all_devices():
    logger.info("Getting all devices")
    query = device_table.select()
    #logger.debug(query)
    return await database.fetch_all(query)


@router.get("/devices/{id}", response_model=Device, status_code=200)
async def get_device(id: int):
    logger.info(f"Getting device with id {id}")
    query = device_table.select().where(device_table.c.id == id)
    device = await database.fetch_one(query)

    if not device:
        logger.error(f"Device with id {id} not found.")
        raise HTTPException(status_code=404, detail="Device not found.")

    return device