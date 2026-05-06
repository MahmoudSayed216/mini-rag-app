from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from ..helpers.config import get_settings, Settings
from ..controllers import DataController, ProjectController, ProcessController
from ..models import ResponseSignal
import os
import logging
from ..schemas.process_args import ProcessingArgs
from ..models.project_model import ProjectModel
from ..models.data_chunk_model import DataChunkModel
from ..models.db_schemas import DataChunk, Asset
from ..models.assets_model import AssetModel
from ..models.enums.AssetTypeEnums import AssetTypeEnum

logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1", "data"])



@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile, app_settings: Depends = Depends(get_settings)):
    
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)

    project = await project_model.get_or_create_project(project_id=project_id)

    #? WHY DOESN'T THE CONTROLLER OBJECTS TAKE THE PROJECT_ID AS A PARAMETER TOO, I THINK IT'S TOTALLY FINE
    data_controller = DataController()
    print("!!!")
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
        
    ## store the assets into the db
    asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
    asset_resource = Asset(
         asset_project_id=project.id,
         asset_type=AssetTypeEnum.FILE.value,
         asset_name=file_id,
         asset_size=os.path.getsize(unique_file_path),
    )

    asset_record = await  asset_model.create_asset(asset=asset_resource)

    return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "signal" : ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,
                "file_id" : str(asset_record.id),
            }
        )




@data_router.post("/process/{project_id}")
async def process_file(request: Request, project_id: str, process_args: ProcessingArgs):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)

    project = await project_model.get_or_create_project(project_id=project_id)


    process_controller = ProcessController(project_id=project_id)
    file_chunks = process_controller.process_file_content(process_args)

        
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                    "signal": ResponseSignal.FILE_PROCESSING_FAILED.value
                }                
            )
    
    chunks = [
        DataChunk(text=chunk.page_content,
                  metadata=chunk.metadata,
                  order=i+1,
                  project_id=project.id)
        for i, chunk in enumerate(file_chunks)
    ]
    
    chunk_model = await DataChunkModel.create_instance(db_client=request.app.db_client)
    reset = -1
    if process_args.do_reset:
        reset = await chunk_model.delete_chunk_by_project_id(project_id=project.id) 

    res = await chunk_model.insert_many_chunks(chunks=chunks)

    return JSONResponse(
         status_code=status.HTTP_200_OK,
         content={
              "singal": ResponseSignal.FILE_PROCESSED_SUCCESSFULLY.value,
              "n_chunks": res,
              "reset": reset
         }
    )