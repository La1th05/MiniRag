from fastapi import FastAPI,APIRouter, Depends
from helpers.config import get_settings, Settings

router=APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)

@router.get("/")
async def welcome(app_settings=Depends(get_settings)):
    app_settings= get_settings()
    app_name= app_settings.APP_NAME
    app_version=app_settings.APP_VERSION
    
    return {
        "App Name":app_name,
        "App verion":app_version
    }
