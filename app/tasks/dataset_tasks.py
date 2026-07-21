from app.celery_app import celery_app

from app.database.database import SessionLocal

from app.services.processing_service import process_dataset


@celery_app.task(name="process_dataset_task")
def process_dataset_task(batch_id: int):
    """
    Background task that processes a dataset batch.
    """

    db = SessionLocal()

    try:
        process_dataset(
            db=db,
            batch_id=batch_id
        )

    finally:
        db.close()