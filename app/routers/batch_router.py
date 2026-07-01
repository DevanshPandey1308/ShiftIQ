from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.batch_schema import (
    BatchCreate,
    BatchUpdate,
    BatchResponse
)
from app.services.batch_service import (
    create_batch,
    get_all_batches,
    get_batch_by_id,
    update_batch,
    delete_batch
)

router = APIRouter(
    prefix="/batches",
    tags=["batches"]
)

@router.post("/", response_model=BatchResponse)
def register_batch(
    batch: BatchCreate,
    db: Session = Depends(get_db)
):
    return create_batch(db, batch)

@router.get("/", response_model=list[BatchResponse])
def read_all_batches(
    db: Session = Depends(get_db)
):
    return get_all_batches(db)

@router.get("/{batch_id}", response_model=BatchResponse)
def read_batch(
    batch_id: int,
    db: Session = Depends(get_db)
):
    return get_batch_by_id(db, batch_id)

@router.put("/{batch_id}", response_model=BatchResponse)
def update_existing_batch(
    batch_id: int,
    batch: BatchUpdate,
    db: Session = Depends(get_db)
):
    return update_batch(
        db,
        batch_id,
        batch
    )

@router.delete("/{batch_id}")
def delete_existing_batch(
    batch_id: int,
    db: Session = Depends(get_db)
):
    return delete_batch(
        db,
        batch_id
    )