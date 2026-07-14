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


class DashboardBatchResponse(BaseModel):
    id: int

    dataset_id: int

    status: str

    health_score: float | None

    processing_started_at: datetime | None

    processing_completed_at: datetime | None

    model_config = {
        "from_attributes": True
    }

class HealthTrendResponse(BaseModel):
    batch_id: int

    health_score: float | None

    processing_completed_at: datetime | None

class AlertAnalyticsResponse(BaseModel):
    total_alerts: int

    high_alerts: int

    medium_alerts: int

    low_alerts: int

class ModelAnalyticsResponse(BaseModel):
    model_id: int

    model_name: str

    total_batches: int

    average_health_score: float | None

    latest_batch_status: str | None