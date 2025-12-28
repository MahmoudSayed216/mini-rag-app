from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
from models import ResponseSignal
import os
import logging
from .schemas.data import ProcessRequest



logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])



@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str, file: UploadFile, app_settings: Depends = Depends(get_settings)):
    
    data_controller = DataController()
    is_valid, response_signal = data_controller.validate_file(file)


    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal" : ResponseSignal.FILE_UPLOAD_FAILED.value,
            }
        )


    project_controller = ProjectController()

    project_dir_path = project_controller.get_project_path(project_id=project_id) # creates a dir for project id, and returns its path
    unique_file_path, file_id = data_controller.generate_unique_filepath(file.filename, project_id)
    print("unique id:\t" + file_id)
    await data_controller.write_file_to_disk(file, unique_file_path)

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "signal" : ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,
                "file_id" : file_id
            }
        )




@data_router.post("/process/{project_id}")
async def process_file(project_id: str, process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "file_id" : file_id,
            "chunk_size":chunk_size,
            "overlap_size" : overlap_size,
            "do_reset" : do_reset
        }                
        )