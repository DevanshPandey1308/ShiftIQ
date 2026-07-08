from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.alert_schema import (
    AlertResponse
)

from app.services.alert_service import (
    get_all_alerts,
    get_alert_by_id,
    get_alerts_by_batch
)

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


@router.get(
    "/",
    response_model=list[AlertResponse]
)
def read_all_alerts(
    db: Session = Depends(get_db)
):
    return get_all_alerts(db)


@router.get(
    "/{alert_id}",
    response_model=AlertResponse
)
def read_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):
    return get_alert_by_id(
        db,
        alert_id
    )


@router.get(
    "/batch/{batch_id}",
    response_model=list[AlertResponse]
)
def read_batch_alerts(
    batch_id: int,
    db: Session = Depends(get_db)
):
    return get_alerts_by_batch(
        db,
        batch_id
    )