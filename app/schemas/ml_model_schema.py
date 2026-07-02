from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MLModelCreate(BaseModel):
    name: str
    description: Optional[str] = None
    problem_type: str
    target_column: str
    model_type: str


class MLModelUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    problem_type: Optional[str] = None
    target_column: Optional[str] = None
    model_type: Optional[str] = None
    version: Optional[str] = None
    environment: Optional[str] = None
    status: Optional[str] = None


class MLModelResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    problem_type: str
    target_column: str
    model_type: str
    version: str
    environment: str
    status: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )