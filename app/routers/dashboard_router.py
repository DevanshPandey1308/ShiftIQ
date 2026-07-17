from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.dashboard_schema import (
    DashboardSummaryResponse
)

from app.services.dashboard_service import (
    get_dashboard_summary
)

from app.schemas.dashboard_schema import (
    DashboardSummaryResponse,
    DashboardBatchResponse,
    HealthTrendResponse,
    AlertAnalyticsResponse,
    ModelAnalyticsResponse,
    RecentActivityResponse
)

from app.services.dashboard_service import (
    get_dashboard_summary,
    get_recent_batches,
    get_health_trend,
    get_alert_analytics,
    get_model_analytics,
    get_recent_activity
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse
)
def read_dashboard_summary(
    db: Session = Depends(get_db)
):
    return get_dashboard_summary(db)

@router.get(
    "/batches",
    response_model=list[DashboardBatchResponse]
)
def read_recent_batches(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_recent_batches(
        db,
        limit
    )

@router.get(
    "/health-trend",
    response_model=list[HealthTrendResponse]
)
def read_health_trend(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_health_trend(
        db,
        limit
    )

@router.get(
    "/alert-analytics",
    response_model=AlertAnalyticsResponse
)
def read_alert_analytics(
    db: Session = Depends(get_db)
):
    return get_alert_analytics(db)

@router.get(
    "/model-analytics",
    response_model=list[ModelAnalyticsResponse]
)
def read_model_analytics(
    db: Session = Depends(get_db)
):
    return get_model_analytics(db)

@router.get(
    "/recent-activity",
    response_model=list[RecentActivityResponse]
)
def read_recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_recent_activity(
        db,
        limit
    )