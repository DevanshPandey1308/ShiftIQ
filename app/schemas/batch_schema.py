from datetime import datetime

from pydantic import BaseModel


class BatchCreate(BaseModel):
    dataset_id: int


class BatchUpdate(BaseModel):
    status: str


class BatchResponse(BaseModel):
    id: int
    dataset_id: int
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }