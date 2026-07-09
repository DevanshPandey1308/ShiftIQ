from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ai_insight import AIInsight


def create_ai_insight(
    db: Session,
    batch_id: int,
    insight: str,
    recommendation: str
):
    ai_insight = AIInsight(
        batch_id=batch_id,
        insight=insight,
        recommendation=recommendation
    )

    db.add(ai_insight)
    db.commit()
    db.refresh(ai_insight)

    return ai_insight


def get_all_ai_insights(
    db: Session
):
    return db.query(AIInsight).all()


def get_ai_insight_by_id(
    db: Session,
    insight_id: int
):
    ai_insight = db.query(AIInsight).filter(
        AIInsight.id == insight_id
    ).first()

    if not ai_insight:
        raise HTTPException(
            status_code=404,
            detail="AI Insight not found."
        )

    return ai_insight


def get_ai_insights_by_batch(
    db: Session,
    batch_id: int
):
    return db.query(AIInsight).filter(
        AIInsight.batch_id == batch_id
    ).all()