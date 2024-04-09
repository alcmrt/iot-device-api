from datetime import datetime
from fastapi import APIRouter
from iot_device_api.models.device import Device, DeviceIn


router = APIRouter()
device_table = []

@router.post("/devices", response_model=Device)
async def create_device(post: DeviceIn):
    data = post.model_dump()
    last_record_id = len(device_table)

    data["createTime"] = datetime.now()
    data["updateTime"] = datetime.now()

    new_device = {"id": last_record_id, **data}
    #device_table[last_record_id] = new_device
    device_table.append(new_device)

    return new_device


@router.get("/devices", response_model=list[Device])
async def get_all_devices():
    return device_table



@router.get("/devices/{id}", response_model=Device)
async def get_device(id: int):
    for device in device_table:
        if device["id"] == id:
            return device