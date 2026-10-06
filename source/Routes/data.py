from fastapi import FastAPI,APIRouter, Depends, UploadFile, status,Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import (DataController,BaseController,
                         ProjectController,ProcessController)
from models.ProjectModel import ProjectModel
from models.ChunckModel import ChunkModel
from .schemas.data import ProcessRequest 
from models.db_shcemes.DataChunck import DataChunck
from models.enums.ResponseEnums import ResponseSignal
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
async def upload_data(request:Request,Project_id:str,file:UploadFile,
                      app_settings:Settings=Depends(get_settings)):
    
    project_model=ProjectModel(
        db_client=request.app.db_client
    )
    project=await project_model.get_project_or_create_one(
        project_id=Project_id
    )
    
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
        "file_id":file_id,
    }
    ) 
    
@data_router.post("/process/{project_id}")
async def process_endpoint(request:Request,project_id:str,process_request:ProcessRequest):
    
    file_id=process_request.filed_id
    process_controller=ProcessController(project_id=project_id)
    file_content=process_controller.get_file_content(file_id=file_id)
    
    chunk_size=process_request.chunck_size
    overlap_size=process_request.overlap_size
    do_reset=process_request.do_reset
    
    project_model=ProjectModel(
        db_client=request.app.db_client
        )
    
    project= await project_model.get_project_or_create_one(
        project_id=project_id
    )
    chunk_model=ChunkModel(
            db_client=request.app.db_client
        )
    
    if do_reset == 1 :
       _ = await chunk_model.delete_chunks_by_project_id(project_id=project_id)

    file_chunks=process_controller.process_file_content(file_content=file_content,file_id=file_id,
                             chunk_size=chunk_size,overlap_size=overlap_size)
    
    if file_chunks is None or len(file_chunks) == 0 :
        return JSONResponse(
            status_code= status.HTTP_400_BAD_REQUEST,
            content={"signal":ResponseSignal.PROCESSING_FAILED.value}
        )
    
    file_chunks_records = [
        DataChunck(
            chunck_text=chunk.page_content,
            meta_data=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id=str(project.id)
        )
        for i,chunk in enumerate(file_chunks)
    ]
    
    no_records=await chunk_model.insert_many_chunks(chunks=file_chunks_records)
    
    return JSONResponse(
        content={
            "signal":ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted chunk": no_records
        }
    )