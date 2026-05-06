from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId


class DataChunk(BaseModel):
    
    id: Optional[ObjectId] = Field(None, alias="_id")
    # project_id, order, chunk text, metadata
    text: str = Field(..., min_length=1)
    metadata: dict
    order: int = Field(..., gt=0)
    project_id : ObjectId


    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexes(cls):

        return [
            {
                "key": [
                    ("chunk_project_id", 1)
                ],
                "name": "chunk_project_id_index_1",
                "unique": False
            }
        ]