from pydantic import BaseModel, Field


class DatasetCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    owner_id: int


class DatasetUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    owner_id: int


class DatasetResponse(BaseModel):
    id: int
    name: str
    owner_id: int

    model_config = {
        "from_attributes": True
    }