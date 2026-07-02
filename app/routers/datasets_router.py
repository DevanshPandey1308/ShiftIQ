from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, UploadFile, File, Form

from app.database.dependencies import get_db
from app.schemas.dataset_schema import (
    DatasetCreate,
    DatasetUpdate,
    DatasetResponse,
)
from app.services.dataset_service import (
    create_dataset,
    get_all_datasets,
    get_dataset_by_id,
    update_dataset,
    delete_dataset,
    get_dataset_profile
)

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/", response_model=DatasetResponse)
def register_dataset(
    name: str = Form(...),
    owner_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return create_dataset(
        db,
        name,
        owner_id,
        file
    )


@router.get("/", response_model=list[DatasetResponse])
def read_all_datasets(db: Session = Depends(get_db)):
    return get_all_datasets(db)


@router.get("/{dataset_id}", response_model=DatasetResponse)
def read_dataset(dataset_id: int, db: Session = Depends(get_db)):
    return get_dataset_by_id(db, dataset_id)

@router.get("/{dataset_id}/profile")
def read_dataset_profile(
    dataset_id: int,
    db: Session = Depends(get_db)
):
    return get_dataset_profile(
        db,
        dataset_id
    )


@router.put("/{dataset_id}", response_model=DatasetResponse)
def update_existing_dataset(
    dataset_id: int,
    dataset: DatasetUpdate,
    db: Session = Depends(get_db),
):
    return update_dataset(db, dataset_id, dataset)


@router.delete("/{dataset_id}")
def delete_existing_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
):
    return delete_dataset(db, dataset_id)