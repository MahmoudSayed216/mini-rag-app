from helpers.config import get_settings, Settings
import os


class BaseController:
    def __init__(self):
        self.app_settings:Settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        print("self.base_dir:\t",self.base_dir)
        # self.files_dir = os.path.join(self.base_dir, )
        self.files_dir = self.base_dir+"/assets/files"
        print("self.files_dir:\t",self.files_dir)



#/home/mahmoud-sayed/Desktop/Code/Python/mini-rag/mini-rag/src/assets/files/1
#/home/mahmoud-sayed/Desktop/Code/Python/mini-rag/mini-rag/assets/files