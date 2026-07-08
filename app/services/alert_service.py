from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.alert import Alert


def create_alert(
    db: Session,
    batch_id: int,
    severity: str,
    message: str
):
    alert = Alert(
        batch_id=batch_id,
        severity=severity,
        message=message
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def get_all_alerts(
    db: Session
):
    return db.query(Alert).all()


def get_alert_by_id(
    db: Session,
    alert_id: int
):
    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found."
        )

    return alert


def get_alerts_by_batch(
    db: Session,
    batch_id: int
):
    return db.query(Alert).filter(
        Alert.batch_id == batch_id
    ).all()