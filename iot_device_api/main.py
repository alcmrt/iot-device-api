from fastapi import FastAPI
from iot_device_api.routers.device import router as device_router


app = FastAPI()
app.include_router(device_router)

@app.get("/")
async def root():
    return {"message": "Hellow World!"}
