from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController
from models import ResponseSignal

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
    

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "outer signal" : ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,
                "inner singal" : response_signal
            }
        )