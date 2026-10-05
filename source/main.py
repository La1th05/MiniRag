from fastapi import FastAPI
from Routes import base,data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings

app=FastAPI()

@app.on_event("startup")
async def start_up():
    settings = get_settings()
    
    app.mongo_connection = AsyncIOMotorClient(settings.MONOGODB_URL)
    app.db_client = app.mongo_connection[settings.MONGODB_DB]

app.include_router(base.router)
app.include_router(data.data_router)


@app.on_event("shutdown")
async def shutdown_db():
    app.mongo_connection.close()

 