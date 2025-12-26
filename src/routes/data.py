from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
from models import ResponseSignal
import aiofiles
import os

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])



@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str, file: UploadFile, app_settings: Depends = Depends(get_settings)):
    controller = DataController()

    is_valid, response_signal = controller.validate_file(file)


    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "outer signal" : ResponseSignal.FILE_UPLOAD_FAILED.value,
                "inner singal" : response_signal
            }
        )
    

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    project_file_path = os.path.join(project_dir_path, file.filename)

    
    async with aiofiles.open(project_file_path, 'wb') as f:
        while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
            await f.write(chunk)


    

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "outer signal" : ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,
                "inner singal" : response_signal
            }
        )