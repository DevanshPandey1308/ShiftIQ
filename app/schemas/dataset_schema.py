from pydantic import BaseModel, Field
from datetime import datetime


class DatasetCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    owner_id: int


class DatasetUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    owner_id: int


class DatasetResponse(BaseModel):
    id: int
    name: str
    file_path: str
    owner_id: int

    row_count: int | None
    column_count: int | None

    created_at: datetime

    model_config = {
        "from_attributes": True
    }