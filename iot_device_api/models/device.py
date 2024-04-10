"""
Contains device pydantic models.
"""

from datetime import datetime
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
