from datetime import datetime

from pydantic import BaseModel


class AlertResponse(BaseModel):
    id: int

    batch_id: int

    severity: str

    message: str

    is_resolved: bool

    created_at: datetime

    model_config = {
        "from_attributes": True
    }