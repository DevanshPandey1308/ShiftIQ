from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.batch import Batch
from app.models.dataset import Dataset
from app.schemas.batch_schema import (
    BatchCreate,
    BatchUpdate
)


from app.services.processing_service import process_dataset
from app.database.database import SessionLocal

def create_batch(
    db: Session,
    batch: BatchCreate
):
    dataset = db.query(Dataset).filter(
        Dataset.id == batch.dataset_id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    new_batch = Batch(
        dataset_id=batch.dataset_id,
        status="Pending"
    )

    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)

    # Create a fresh database session for processing
    processing_db = SessionLocal()

    try:
        process_dataset(
            db=processing_db,
            batch_id=new_batch.id
        )
    finally:
        processing_db.close()

    db.refresh(new_batch)

    return new_batch

def get_all_batches(db: Session):
    return db.query(Batch).all()

def get_batch_by_id(
    db: Session,
    batch_id: int
):
    batch = db.query(Batch).filter(
        Batch.id == batch_id
    ).first()

    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found."
        )

    return batch

def update_batch(
    db: Session,
    batch_id: int,
    batch_data: BatchUpdate
):
    batch = db.query(Batch).filter(
        Batch.id == batch_id
    ).first()

    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found."
        )

    batch.status = batch_data.status

    db.commit()
    db.refresh(batch)

    return batch

def delete_batch(
    db: Session,
    batch_id: int
):
    batch = db.query(Batch).filter(
        Batch.id == batch_id
    ).first()

    if not batch:
        raise HTTPException(
            status_code=404,
            detail="Batch not found."
        )

    db.delete(batch)
    db.commit()

    return {
        "message": "Batch deleted successfully."
    }