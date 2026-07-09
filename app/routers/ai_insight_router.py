from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.ai_insight_schema import (
    AIInsightResponse
)

from app.services.ai_insight_service import (
    get_all_ai_insights,
    get_ai_insight_by_id,
    get_ai_insights_by_batch
)

router = APIRouter(
    prefix="/ai-insights",
    tags=["AI Insights"]
)


@router.get(
    "/",
    response_model=list[AIInsightResponse]
)
def read_all_ai_insights(
    db: Session = Depends(get_db)
):
    return get_all_ai_insights(db)


@router.get(
    "/{insight_id}",
    response_model=AIInsightResponse
)
def read_ai_insight(
    insight_id: int,
    db: Session = Depends(get_db)
):
    return get_ai_insight_by_id(
        db,
        insight_id
    )


@router.get(
    "/batch/{batch_id}",
    response_model=list[AIInsightResponse]
)
def read_batch_ai_insights(
    batch_id: int,
    db: Session = Depends(get_db)
):
    return get_ai_insights_by_batch(
        db,
        batch_id
    )