from datetime import datetime

from pydantic import BaseModel


class AIInsightResponse(BaseModel):
    id: int

    batch_id: int

    insight: str

    recommendation: str

    created_at: datetime

    model_config = {
        "from_attributes": True
    }