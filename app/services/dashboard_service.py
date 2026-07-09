from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ml_model import MLModel
from app.models.dataset import Dataset
from app.models.batch import Batch
from app.models.alert import Alert


def get_dashboard_summary(
    db: Session
):
    total_models = db.query(
        MLModel
    ).count()

    total_datasets = db.query(
        Dataset
    ).count()

    total_batches = db.query(
        Batch
    ).count()

    completed_batches = db.query(
        Batch
    ).filter(
        Batch.status == "Completed"
    ).count()

    failed_batches = db.query(
        Batch
    ).filter(
        Batch.status == "Failed"
    ).count()

    active_alerts = db.query(
        Alert
    ).filter(
        Alert.is_resolved.is_(False)
    ).count()

    average_health_score = db.query(
        func.avg(
            Batch.health_score
        )
    ).scalar()

    latest_batch = db.query(
        Batch
    ).order_by(
        Batch.id.desc()
    ).first()

    if average_health_score is not None:
        average_health_score = round(
            float(average_health_score),
            2
        )

    return {
        "total_models": total_models,
        "total_datasets": total_datasets,
        "total_batches": total_batches,
        "completed_batches": completed_batches,
        "failed_batches": failed_batches,
        "active_alerts": active_alerts,
        "average_health_score": average_health_score,
        "latest_batch": latest_batch
    }