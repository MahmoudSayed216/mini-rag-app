from fastapi import UploadFile
from .BaseController import BaseController
from .ProjectController import ProjectController
from models import ResponseSignal
import os
import re



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
            



        

    def clean_file_name(self, file_name:str):
        return re.sub(r'[^\w.]', '', file_name.strip()).replace(" ", "_")
        
