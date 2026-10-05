from pydantic import BaseModel, Field , validator
from typing import Optional
from bson.objectid import ObjectId

class DataChunck(BaseModel):
    _id: Optional[ObjectId]
    chunck:str = Field(...,min_length=1)
    meta_data: dict
    chunk_order:int = Field (...,gt=0)
    chunk_project_id = ObjectId
    
    
    class Config:
        arbitrary_types_allowed=True