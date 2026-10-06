from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson.objectid import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]
class DataChunck(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id",default=None)
    chunck_text:str = Field(...,min_length=1)
    meta_data: dict
    chunk_order:int = Field (...,gt=0)
    chunk_project_id : str
    
    
    model_config={
            "populate_by_name":True,
            "arbitrary_types_allowed":True
        }