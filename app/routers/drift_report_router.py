from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.drift_report_schema import (
    DriftReportResponse,
    FeatureRankingResponse,
    BatchComparisonResponse
)

from app.services.drift_report_service import (
    get_all_drift_reports,
    get_drift_report_by_id,
    get_drift_report_by_batch,
    get_feature_ranking_by_batch,
    compare_drift_reports
)

router = APIRouter(
    prefix="/drift-reports",
    tags=["Drift Reports"]
)


@router.get(
    "/",
    response_model=list[DriftReportResponse]
)
def read_all_drift_reports(
    db: Session = Depends(get_db)
):
    return get_all_drift_reports(db)



@router.get(
    "/compare",
    response_model=BatchComparisonResponse
)
def compare_reports(
    batch_a: int,
    batch_b: int,
    db: Session = Depends(get_db)
):
    return compare_drift_reports(
        db,
        batch_a,
        batch_b
    )

@router.get(
    "/batch/{batch_id}",
    response_model=DriftReportResponse
)
def read_batch_drift_report(
    batch_id: int,
    db: Session = Depends(get_db)
):
    return get_drift_report_by_batch(
        db,
        batch_id
    )


@router.get(
    "/batch/{batch_id}/features",
    response_model=list[FeatureRankingResponse]
)
def read_feature_ranking(
    batch_id: int,
    db: Session = Depends(get_db)
):
    return get_feature_ranking_by_batch(
        db,
        batch_id
    )



@router.get(
    "/{report_id}",
    response_model=DriftReportResponse
)
def read_drift_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    return get_drift_report_by_id(
        db,
        report_id
    )