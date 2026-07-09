from datetime import datetime

from pydantic import BaseModel


class LatestBatchResponse(BaseModel):
    id: int

    status: str

    health_score: float | None

    processing_completed_at: datetime | None

    model_config = {
        "from_attributes": True
    }


class DashboardSummaryResponse(BaseModel):
    total_models: int

    total_datasets: int

    total_batches: int

    completed_batches: int

    failed_batches: int

    active_alerts: int

    average_health_score: float | None

    latest_batch: LatestBatchResponse | None