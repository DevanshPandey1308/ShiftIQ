from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.models.user import User
from app.schemas.dataset_schema import (
    DatasetCreate,
    DatasetUpdate
)


def create_dataset(db: Session, dataset: DatasetCreate):
    owner = db.query(User).filter(User.id == dataset.owner_id).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found."
        )

    new_dataset = Dataset(
        name=dataset.name,
        owner_id=dataset.owner_id
    )

    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)

    return new_dataset


def get_all_datasets(db: Session):
    return db.query(Dataset).all()


def get_dataset_by_id(db: Session, dataset_id: int):
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    return dataset


def update_dataset(
    db: Session,
    dataset_id: int,
    dataset_data: DatasetUpdate
):
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    owner = db.query(User).filter(
        User.id == dataset_data.owner_id
    ).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found."
        )

    dataset.name = dataset_data.name
    dataset.owner_id = dataset_data.owner_id

    db.commit()
    db.refresh(dataset)

    return dataset


def delete_dataset(db: Session, dataset_id: int):
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    db.delete(dataset)
    db.commit()

    return {
        "message": "Dataset deleted successfully."
    }