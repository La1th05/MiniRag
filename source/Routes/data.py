from fastapi import FastAPI,APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController,BaseController,ProjectController
import os
import aiofiles
import logging


data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["api","data"]
)
logger=logging.getLogger("uvicorn.error")
data_con=DataController()

@data_router.post("/upload/{Project_id}")
async def upload_data(Project_id:str,file:UploadFile,
                      app_settings:Settings=Depends(get_settings)):
    is_valid,result_signal=data_con.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":result_signal
            }
        )
    project_dir_path=ProjectController().get_project_path(project_id=Project_id)
    file_path=data_con.generate_new_file_name(
       project_path=project_dir_path,
       org_file_name=file.filename
    )
    try:
        async with aiofiles.open(file_path,"wb") as f:
            while chunk:= await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e :
        logger.error(f"Error while uploding the file {e}")
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":result_signal
            }
        )
    
    return JSONResponse(
        {
        "signal":result_signal
    }
    ) 