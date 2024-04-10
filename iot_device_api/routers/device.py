import logging

from datetime import datetime
from fastapi import APIRouter, HTTPException
from sqlalchemy import asc, desc, func, select, update
from iot_device_api.models.device import Device, Device2, DeviceCreate, LocationBase, Location, LocationIn
from iot_device_api.database import device_table, location_table, database


router = APIRouter()
logger = logging.getLogger(__name__)



@router.post("/devices", tags=["Devices"], response_model=Device, status_code=201)
async def create_device(device: DeviceCreate):
    """
    _Add a new device and location information of this device._
        
    Returns:
    _JSON object of the new device._
    """

    logger.info("Creating a new device...")
    
    data = device.model_dump()
    data["createTime"] = datetime.now()
    data["updateTime"] = datetime.now()

    # Insert device data
    query = device_table.insert().values(
        name=data["name"],
        locationType=data["locationType"],
        category=data["category"],
        status=data["status"],
        createTime=data["createTime"],
        updateTime=data["updateTime"]
    )

    logger.debug(query)
    last_device_id = await database.execute(query)
    
    # create location object
    location = LocationBase(
        device_id=last_device_id,
        latitude=data["latitude"],
        longitude=data["longitude"],
        createTime=data["createTime"],
        updateTime=data["updateTime"]
    )
    # add device locations to locations table
    query = location_table.insert().values(location.model_dump())
    logger.debug(query)
    await database.execute(query)
    
    new_device = {"id": last_device_id, **data}
    return new_device


@router.get("/devices", tags=["Devices"], response_model=list[Device2], status_code=200)
async def get_all_devices():
    """
    _Get list of all devices_
    
    Returns:
     * _JSON_: _List of device objects._
    """
    logger.info("Getting all devices")
    query = device_table.select()
    logger.debug(query)
    return await database.fetch_all(query)


@router.get("/devices/{device_id}/locations", tags=["Device Locations"], response_model=list[Location])
async def get_location_history_by_device(device_id: int):
    """
    Endpoint to get location history for a device.

    Parameters:

    - device_id (int): The id of the device.
    """
    logger.info("Getting location history by device_id")
    
    #Build the query to fetch locations for the device
    location_query = select(location_table).where(location_table.c.device_id == device_id)
    locations = await database.fetch_all(query=location_query)
    logger.debug(location_query)
    
    # Check if any locations exist for the device
    if not locations:
        logger.error(f"No locations found for device with id {device_id}")
        raise HTTPException(status_code=404, detail="No locations found for this device")

    # Return the list of locations
    return locations


@router.post("/devices/{device_id}/locations", tags=["Device Locations"])
async def add_device_location(device_id: int, location_data: LocationIn):
    """_Add new location for existing device._

    Parameters:
        - device_id (int): _The id of th device._
    
    Raises:
        HTTPException: _Device Not Found_
    """

    # Check if the device exists
    device_query = device_table.select().where(device_table.c.id == device_id)
    device = await  database.fetch_one(device_query)
    if not device:
        logger.error(f"Device with id {id} not found.")
        raise HTTPException(status_code=404, detail="Device not found")

    location_data = location_data.model_dump()
    location_data["updateTime"] = datetime.now()
    location_data["createTime"] = datetime.now()

    # Insert new location with device_id
    insert_query = location_table.insert().values(
        device_id=device_id,
        **location_data,
    )

    # Execute the update query asynchronously
    await database.execute(insert_query)
    return {"message": "Device location inserted successfully"}



@router.get("/devices/lastlocations", tags=["Device Locations"])
async def get_last_location_of_all_devices():
    """_Get last location for all devices._
    """

    # Subquery to get the latest create time for each device
    subquery = select(
        location_table.c.device_id,
        func.max(location_table.c.createTime).label("maxCreateTime")
    ).group_by(
        location_table.c.device_id
    ).alias("subquery")

    # Main query to select the latest locations
    location_query = select(
        location_table
    ).where(
        (location_table.c.device_id == subquery.c.device_id) &
        (location_table.c.createTime == subquery.c.maxCreateTime)
    )

    # Execute the query asynchronously
    locations = await database.fetch_all(location_query.order_by(asc(location_table.c.device_id)))

    return locations


@router.get("/devices/{id}", tags=["Devices"], response_model=Device2, status_code=200)
async def get_device(id: int):
    logger.info(f"Getting device with id {id}")
    query = device_table.select().where(device_table.c.id == id)
    device = await database.fetch_one(query)

    if not device:
        logger.error(f"Device with id {id} not found.")
        raise HTTPException(status_code=404, detail="Device not found.")

    return device


@router.delete("/devices/{id}", tags=["Devices"], status_code=201)
async def delete_device(id: int):
    """
    _Delete device with given id._
    _Deletes device and locations of the device._

    Parameters:
    - id (int): _the id of the device._
    """

    # Check if the device exists
    device_query = device_table.select().where(device_table.c.id == id)
    device = await  database.fetch_one(device_query)
    if not device:
        logger.error(f"Device with id {id} not found.")
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Delete locations for the device first
    logger.info(f"Deleting locations of the device with id {id}")
    location_delete_query = location_table.delete().where(location_table.c.device_id == id)
    await database.execute(location_delete_query)
    
    # Delete the device itself
    logger.info(f"Deleting the device with id {id}")
    device_delete_query = device_table.delete().where(device_table.c.id == id)
    await database.execute(device_delete_query)

    return {"detail": "Device deleted succesfully"}
