from .BaseController import BaseController
import os

class ProjectController(BaseController):

    def __init__(self):
        super().__init__()

    
    def get_project_path(self, project_id):
        project_path = os.path.join(self.projects_dir, str(project_id))
        print("self.project_path:\t",project_path)

        if not os.path.exists(project_path):
            os.makedirs(project_path)


        return project_path


    