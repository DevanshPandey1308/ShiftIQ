from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.utils.file_handler import save_uploaded_file
from fastapi import UploadFile
from app.utils.csv_processor import extract_csv_metadata

from app.models.dataset import Dataset
from app.models.user import User
from app.schemas.dataset_schema import (
    DatasetCreate,
    DatasetUpdate
)

import pandas as pd

from app.utils.profiler import (
    generate_dataset_profile,
    get_numeric_statistics,
    get_categorical_statistics
)


def create_dataset(
    db: Session,
    name: str,
    owner_id: int,
    file: UploadFile
):
    owner = db.query(User).filter(User.id == owner_id).first()

    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found."
        )

    metadata = extract_csv_metadata(file)
    file_path = save_uploaded_file(file)

    new_dataset = Dataset(
    name=name,
    owner_id=owner_id,
    file_path=file_path,
    row_count=metadata["row_count"],
    column_count=metadata["column_count"]
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

def get_dataset_profile(
    db: Session,
    dataset_id: int
):
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id
    ).first()

    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found."
        )

    df = pd.read_csv(dataset.file_path)

    profile = generate_dataset_profile(df)

    profile["numeric_statistics"] = get_numeric_statistics(df)

    profile["categorical_statistics"] = get_categorical_statistics(df)

    return profile