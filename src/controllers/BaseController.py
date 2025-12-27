from helpers.config import get_settings, Settings
import os
import random
import string


class BaseController:
    def __init__(self):
        self.app_settings:Settings = get_settings()
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.projects_dir = os.path.join(self.base_dir, "assets/projects")


        
    def generate_random_string(self, length:int=12):
        return "".join(random.choices(string.ascii_lowercase+string.digits, k=length))
#/home/mahmoud-sayed/Desktop/Code/Python/mini-rag/mini-rag/src/assets/files/1
#/home/mahmoud-sayed/Desktop/Code/Python/mini-rag/mini-rag/assets/files