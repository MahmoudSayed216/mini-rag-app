from .base_data_model import BaseDataModel
from .enums.DatabaseCollectionsEnum import DBCollectionsEnum
from .db_schemas import Project
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticCollection


class ProjectModel(BaseDataModel):
    
    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_collection()
        return instance
    
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection :AgnosticCollection= self.db_client[DBCollectionsEnum.PROJECTS_COLLECTION.value]

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DBCollectionsEnum.PROJECTS_COLLECTION.value not in all_collections:
            self.collection :AgnosticCollection= self.db_client[DBCollectionsEnum.PROJECTS_COLLECTION.value]
            indexes = Project.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    keys= index["key"],
                    name= index["name"],
                    unique= index["unique"]
                )




    async def create_project(self, project:Project) -> Project:
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        project._id = result.inserted_id
        return project
    

    async def get_or_create_project(self, project_id: str) -> Project:
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