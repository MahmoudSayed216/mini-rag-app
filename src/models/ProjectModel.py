from .BaseDataModel import BaseDataModel
from .enums.DatabaseCollectionsEnum import DBCollectionsEnum
from .db_schemas import Project
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticCollection


class ProjectModel(BaseDataModel):
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection :AgnosticCollection= self.db_client[DBCollectionsEnum.PROJECTS_COLLECTION]


    async def create_project(self, project:Project) -> Project:
        result = await self.collection.insert_one(project.dict())
        project._id = result.inserted_id
        return project
    

    async def get_or_create_project(self, project_id:str) -> Project:
        record = await self.collection.find_one({'project_id':project_id})

        if record is None:
            new_project = Project(project_id=project_id) 
            project = await self.create_project(new_project)
            return project
        
        return Project(**record)
    

    async def get_all_projects(self, page: int = 1, page_size:int = 10):
        total_docs = await self.collection.count_documents({})
        total_pages = total_docs//page_size +  (total_docs%total_pages > 0)

        cursor = self.collection.find().skip((page-1)*page_size).limit(page_size)
        projects = []
        async for doc in cursor:
            projects.append(Project(**doc))

        return projects, total_pages