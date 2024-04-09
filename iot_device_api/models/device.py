"""
Contains device pydantic models.
"""

from pydantic import BaseModel


class DeviceIn(BaseModel):
    name: str
    locationType: str
    category: str
    status: str
    latitude: int
    longitude: int


class Device(DeviceIn):
    id: int
