import requests

from sqlalchemy.orm import Session

from app.models.webhook import Webhook

def send_webhook_notifications(
    db: Session,
    payload: dict
):
    """
    Send the payload to all enabled webhooks.
    A failed webhook should never stop dataset processing.
    """

    webhooks = (
        db.query(Webhook)
        .filter(Webhook.enabled == True)
        .all()
    )

    for webhook in webhooks:
        try:
            response = requests.post(
                webhook.url,
                json=payload,
                timeout=5
            )

            response.raise_for_status()

        except requests.RequestException as e:
            print(
                f"Failed to send webhook '{webhook.name}': {e}"
            )