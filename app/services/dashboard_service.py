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


def get_recent_batches(
    db: Session,
    limit: int = 10
):
    return (
        db.query(Batch)
        .order_by(
            Batch.id.desc()
        )
        .limit(limit)
        .all()
    )

def get_health_trend(
    db: Session,
    limit: int = 10
):
    batches = (
        db.query(Batch)
        .filter(
            Batch.health_score.is_not(None)
        )
        .order_by(
            Batch.processing_completed_at.desc()
        )
        .limit(limit)
        .all()
    )

    batches.reverse()

    return [
        {
            "batch_id": batch.id,
            "health_score": batch.health_score,
            "processing_completed_at": batch.processing_completed_at
        }
        for batch in batches
    ]

def get_alert_analytics(
    db: Session
):
    total_alerts = db.query(
        Alert
    ).count()

    high_alerts = db.query(
        Alert
    ).filter(
        Alert.severity == "HIGH"
    ).count()

    medium_alerts = db.query(
        Alert
    ).filter(
        Alert.severity == "MEDIUM"
    ).count()

    low_alerts = db.query(
        Alert
    ).filter(
        Alert.severity == "LOW"
    ).count()

    return {
        "total_alerts": total_alerts,
        "high_alerts": high_alerts,
        "medium_alerts": medium_alerts,
        "low_alerts": low_alerts
    }

def get_model_analytics(
    db: Session
):
    models = db.query(MLModel).all()

    result = []

    for model in models:

        datasets = db.query(Dataset).filter(
            Dataset.model_id == model.id
        ).all()

        dataset_ids = [dataset.id for dataset in datasets]

        batches = db.query(Batch).filter(
            Batch.dataset_id.in_(dataset_ids)
        ).all()

        total_batches = len(batches)

        health_scores = [
            batch.health_score
            for batch in batches
            if batch.health_score is not None
        ]

        average_health = (
            round(sum(health_scores) / len(health_scores), 2)
            if health_scores
            else None
        )

        latest_batch = (
            sorted(
                batches,
                key=lambda batch: batch.id,
                reverse=True
            )[0]
            if batches
            else None
        )

        result.append({
            "model_id": model.id,
            "model_name": model.name,
            "total_batches": total_batches,
            "average_health_score": average_health,
            "latest_batch_status": (
                latest_batch.status
                if latest_batch
                else None
            )
        })

    return result