from .base_data_model import BaseDataModel
from .enums.DatabaseCollectionsEnum import DBCollectionsEnum
from .db_schemas import Asset
from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticCollection
from bson.objectid import ObjectId


class AssetModel(BaseDataModel):
    
    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_collection()
        return instance
    
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection :AgnosticCollection= self.db_client[DBCollectionsEnum.ASSETS_COLLECTION.value]

    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DBCollectionsEnum.PROJECTS_COLLECTION.value not in all_collections:
            self.collection :AgnosticCollection= self.db_client[DBCollectionsEnum.ASSETS_COLLECTION.value]
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    keys= index["key"],
                    name= index["name"],
                    unique= index["unique"]
                )




    async def create_asset(self, asset: Asset):
        result = await self.collection.insert_one(asset.dict(by_alias=True, exclude_unset=True))
        asset.id = result.inserted_id
        return asset


    async def get_all_project_assets(self, project_id):
        print("tpid: ",type(project_id))
        results = await self.collection.find({'asset_project_id': ObjectId(oid=project_id)}).to_list(None)
        return results