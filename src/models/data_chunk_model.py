from .base_data_model import BaseDataModel
from .db_schemas.data_chunk import DataChunk
from .enums.DatabaseCollectionsEnum import DBCollectionsEnum
from motor.core import AgnosticCollection
from bson.objectid import ObjectId
from pymongo import InsertOne


class DataChunkModel(BaseDataModel):
    
    @classmethod
    async def create_instance(cls, db_client):
        instance = cls(db_client)
        await instance.init_collection()
        return instance
    
    def __init__(self, db_client):
        super().__init__(db_client)
        self.collection: AgnosticCollection  = db_client[DBCollectionsEnum.CHUNKS_COLLECTION.value]

    async def init_collection(self):
        all_collections= await self.db_client.list_collection_names()
        if DBCollectionsEnum.CHUNKS_COLLECTION.value not in all_collections:
            self.collection: AgnosticCollection  = self.db_client[DBCollectionsEnum.CHUNKS_COLLECTION.value]
            indexes = DataChunk.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    keys=index["key"],
                    name=index["name"], 
                    unique=index["unique"]
                )
            


    async def create_chunk(self, chunk: DataChunk):
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        result._id = result.inserted_id
        
        return chunk
    

    async def get_chunk(self, chunk_id: str):
        result = await self.collection.find_one({"_id": ObjectId(chunk_id)})
        if result is None:
            return None
        
        return DataChunk(**result)
    

    async def insert_many_chunks(self, chunks: DataChunk, batch_size: int = 100) -> int:
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i: i+batch_size]
            ops = [
                InsertOne(document=chunk.dict(by_alias=True, exclude_unset=True))
                for chunk in batch
            ]

            await self.collection.bulk_write(ops)

        return len(chunks)
    

    async def delete_chunk_by_project_id(self, project_id: ObjectId): 
        result = await self.collection.delete_many({'project_id': project_id})

        return result.deleted_count