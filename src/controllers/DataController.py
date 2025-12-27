from fastapi import UploadFile, status
from fastapi.responses import JSONResponse
from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ResponseSignal
import os
import re
import aiofiles
import logging
import time

logger = logging.getLogger('uvicorn.error')



class DataController(BaseController):
    
    def __init__(self):
        super().__init__()


    def validate_file(self, file:UploadFile):
        if file.content_type not in self.app_settings.ALLOWED_FILE_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if (file.size) > (self.app_settings.MAX_FILE_SIZE):
            return False, ResponseSignal.MAX_FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATED_SUCCESSFULLY.value

    def generate_unique_filename(self, original_file_name, project_id):
        
        random_key = self.generate_random_string()
        print("Original filename: ", type(original_file_name))
        cleaned_file_name = self.clean_file_name(original_file_name)
        file_dir_path = ProjectController().get_project_path(project_id)

        file_path = os.path.join(file_dir_path, random_key +"_"+ cleaned_file_name)

        while os.path.exists(file_path):
            random_key = self.generate_random_string()
            file_path = os.path.join(file_dir_path, random_key, cleaned_file_name)

        return file_path
            

    async def write_file_to_disk(self, file:UploadFile, project_file_path):
        try:
            async with aiofiles.open(project_file_path, 'wb') as f:
                while chunk := await file.read(self.app_settings.FILE_DEFAULT_CHUNK_SIZE):
                    await f.write(chunk)
        except Exception as e:
            logger.error(f"Error while uploading file: {e}")
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal" : ResponseSignal.FILE_UPLOAD_FAILED.value,
                }
            )
        
        print("file logged successfully")



        

    def clean_file_name(self, file_name:str):
        return re.sub(r'[^\w.]', '', file_name.strip()).replace(" ", "_")
        
