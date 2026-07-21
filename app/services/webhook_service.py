from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.webhook import Webhook
from app.schemas.webhook_schema import (
    WebhookCreate,
    WebhookUpdate
)


def create_webhook(
    db: Session,
    webhook: WebhookCreate
):
    new_webhook = Webhook(
        name=webhook.name,
        url=str(webhook.url),
        enabled=True
    )

    db.add(new_webhook)
    db.commit()
    db.refresh(new_webhook)

    return new_webhook


def get_all_webhooks(db: Session):
    return db.query(Webhook).all()


def get_webhook_by_id(
    db: Session,
    webhook_id: int
):
    webhook = db.query(Webhook).filter(
        Webhook.id == webhook_id
    ).first()

    if not webhook:
        raise HTTPException(
            status_code=404,
            detail="Webhook not found."
        )

    return webhook


def update_webhook(
    db: Session,
    webhook_id: int,
    webhook_data: WebhookUpdate
):
    webhook = db.query(Webhook).filter(
        Webhook.id == webhook_id
    ).first()

    if not webhook:
        raise HTTPException(
            status_code=404,
            detail="Webhook not found."
        )

    update_data = webhook_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "url":
            value = str(value)

        setattr(webhook, key, value)

    db.commit()
    db.refresh(webhook)

    return webhook


def delete_webhook(
    db: Session,
    webhook_id: int
):
    webhook = db.query(Webhook).filter(
        Webhook.id == webhook_id
    ).first()

    if not webhook:
        raise HTTPException(
            status_code=404,
            detail="Webhook not found."
        )

    db.delete(webhook)
    db.commit()

    return {
        "message": "Webhook deleted successfully."
    }