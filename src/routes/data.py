from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from ..helpers.config import get_settings, Settings
from ..controllers import DataController, ProjectController, ProcessController
from ..models import ResponseSignal
import os
import logging
from ..schemas.process_args import ProcessingArgs



logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])



@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str, file: UploadFile, app_settings: Depends = Depends(get_settings)):
    #? WHY DOESN'T THE CONTROLLER OBJECTS TAKE THE PROJECT_ID AS A PARAMETER TOO, I THINK IT'S TOTALLY FINE
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
    try:
        await data_controller.write_file_to_disk(file, unique_file_path) 
    except Exception as e:
            logger.error(f"Error while uploading file: {e}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal" : ResponseSignal.FILE_UPLOAD_FAILED.value,
                }
            )
        

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "signal" : ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,
                "file_id" : file_id
            }
        )




@data_router.post("/process/{project_id}")
async def process_file(project_id: str, process_args: ProcessingArgs):



    process_controller = ProcessController(project_id=project_id)
    file_chunks = process_controller.process_file_content(process_args)

        
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                    "signal": ResponseSignal.FILE_PROCESSING_FAILED.value
                }                
            )
                

    return file_chunks