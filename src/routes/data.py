from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
from models import ResponseSignal
import aiofiles
import os
import logging

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
    

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    # project_file_path = os.path.join(project_dir_path, file.filename)
    project_file_path = data_controller.generate_unique_filename(file.filename, project_id)
    

    try:
        async with aiofiles.open(project_file_path, 'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
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
            }
        )