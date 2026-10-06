from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson.objectid import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]
class Project(BaseModel):
    id:Optional[PyObjectId] = Field(alis="_id",default=None)
    project_id:str = Field(...,min_length=1)
    
    @field_validator('project_id')
    def validate_project_id(cls,value):
        if not value.isalnum():
            raise ValueError("Project ID must be alphanumeric")
        return value

    model_config={
        "populate_by_name":True,
        "arbitrary_types_allowed":True
    }