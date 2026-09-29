from fastapi import FastAPI,APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import (DataController,BaseController,
                         ProjectController,ProcessController)
from .schemas.data import ProcessRequest 
from models.enums import ResponseEnums
import os
import aiofiles
import logging


data_router=APIRouter(
    prefix="/api/v1/data",
    tags=["api","data"]
)
logger=logging.getLogger("uvicorn.error")
data_controller=DataController()

@data_router.post("/upload/{Project_id}")
async def upload_data(Project_id:str,file:UploadFile,
                      app_settings:Settings=Depends(get_settings)):
    is_valid,result_signal=data_controller.validate_uploaded_file(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal":result_signal
            }
        )
    project_dir_path=ProjectController().get_project_path(project_id=Project_id)
    file_path,file_id=data_controller.generate_unique_filepth(
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
        "signal":result_signal,
        "file_id":file_id
    }
    ) 
    
@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str,process_request:ProcessRequest):
    
    file_id=process_request.filed_id
    
    
    process_controller=ProcessController(project_id=project_id)
    file_content=process_controller.get_file_content(file_id=file_id)
    chunk_size=process_request.chunck_size
    overlap_size=process_request.overlap_size
    
    file_chunks=process_controller.process_file_content(file_content=file_content,file_id=file_id,
                             chunk_size=chunk_size,overlap_size=overlap_size)
    
    if file_chunks is None or len(file_chunks) == 0 :
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content={"signal":ResponseEnums.PROCESSING_FAILED.value}
        )
    return file_chunks