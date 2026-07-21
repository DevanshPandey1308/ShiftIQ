from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.dependencies import get_db
from app.schemas.webhook_schema import (
    WebhookCreate,
    WebhookUpdate,
    WebhookResponse
)
from app.services.webhook_service import (
    create_webhook,
    get_all_webhooks,
    get_webhook_by_id,
    update_webhook,
    delete_webhook
)

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"]
)


@router.post(
    "/",
    response_model=WebhookResponse
)
def create_new_webhook(
    webhook: WebhookCreate,
    db: Session = Depends(get_db)
):
    return create_webhook(db, webhook)


@router.get(
    "/",
    response_model=List[WebhookResponse]
)
def read_all_webhooks(
    db: Session = Depends(get_db)
):
    return get_all_webhooks(db)


@router.get(
    "/{webhook_id}",
    response_model=WebhookResponse
)
def read_webhook(
    webhook_id: int,
    db: Session = Depends(get_db)
):
    return get_webhook_by_id(db, webhook_id)


@router.put(
    "/{webhook_id}",
    response_model=WebhookResponse
)
def edit_webhook(
    webhook_id: int,
    webhook: WebhookUpdate,
    db: Session = Depends(get_db)
):
    return update_webhook(
        db,
        webhook_id,
        webhook
    )


@router.delete(
    "/{webhook_id}"
)
def remove_webhook(
    webhook_id: int,
    db: Session = Depends(get_db)
):
    return delete_webhook(
        db,
        webhook_id
    )