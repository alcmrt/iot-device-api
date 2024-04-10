import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
from iot_device_api.routers.device import router as device_router
from iot_device_api.database import database
from iot_device_api.logging_conf import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(device_router)
