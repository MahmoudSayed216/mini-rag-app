from fastapi import UploadFile
from .BaseController import BaseController
from models import ResponseSignal


class DataController(BaseController):
    
    def __init__(self):
        super().__init__()


    def validate_file(self, file:UploadFile):
        if file.content_type not in self.app_settings.ALLOWED_FILE_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if (file.size) > (self.app_settings.MAX_FILE_SIZE):
            return False, ResponseSignal.MAX_FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATED_SUCCESSFULLY.value

        