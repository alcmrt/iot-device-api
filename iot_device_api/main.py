from contextlib import asynccontextmanager
from fastapi import FastAPI
from iot_device_api.routers.device import router as device_router
from iot_device_api.database import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI()
app.include_router(device_router)

@app.get("/")
async def root():
    return {"message": "Hellow World!"}
