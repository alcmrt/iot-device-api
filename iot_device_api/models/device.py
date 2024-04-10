"""
Contains device pydantic models.
"""

from datetime import datetime
from typing import List
from pydantic import BaseModel


class DeviceIn(BaseModel):
    name: str
    locationType: str
    category: str
    status: str
    latitude: int
    longitude: int
    createTime: datetime | None = None
    updateTime: datetime | None = None


class Device(DeviceIn):
    id: int

    class Config:
        from_attributes = True



################################################################################

class LocationBase(BaseModel):
    device_id: int
    latitude: float
    longitude: float
    createTime: datetime
    updateTime: datetime

class LocationIn(BaseModel):
    latitude: float
    longitude: float

class Location(LocationBase):
    id: int

class DeviceBase(BaseModel):
    name: str
    locationType: str
    category: str
    status: str
    createTime: datetime | None = None
    updateTime: datetime | None = None

class Device2(DeviceBase):
    id: int

class DeviceCreate(DeviceBase):
    latitude: float
    longitude: float