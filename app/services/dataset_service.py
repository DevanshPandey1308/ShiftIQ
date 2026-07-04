from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.utils.file_handler import save_uploaded_file
from fastapi import UploadFile
from app.utils.csv_processor import extract_csv_metadata
from app.models.ml_model import MLModel

from app.models.dataset import Dataset
from app.models.user import User
from app.schemas.dataset_schema import DatasetUpdate

import pandas as pd

from app.utils.profiler import (
    generate_dataset_profile,
    get_numeric_statistics,
    get_categorical_statistics
)

from app.models.batch import Batch
from app.services.processing_service import process_dataset


def _create_dataset_with_processing(
    db: Session,
    name: str,
    owner_id: int,
    file_path: str,
    metadata: dict,
    model_id: int | None = None,
    dataset_type: str | None = None
):
    """
    Internal helper to create a dataset,
    create its processing batch,
    and trigger processing.
    """

    dataset = Dataset(
        name=name,
        owner_id=owner_id,
        model_id=model_id,
        dataset_type=dataset_type,
        file_path=file_path,
        row_count=metadata["row_count"],
        column_count=metadata["column_count"]
    )

    db.add(dataset)
    db.commit()
    db.refresh(dataset)

    batch = Batch(
        dataset_id=dataset.id,
        status="Pending"
    )

    db.add(batch)
    db.commit()
    db.refresh(batch)

    process_dataset(
        db,
        batch.id
    )

    return dataset



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

    file.file.seek(0)

    file_path = save_uploaded_file(file)

    return _create_dataset_with_processing(
        db=db,
        name=name,
        owner_id=owner_id,
        file_path=file_path,
        metadata=metadata
    )


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

def register_baseline_dataset(
    db: Session,
    model_id: int,
    name: str,
    file: UploadFile
):
    """
    Register a baseline dataset for an ML Model.
    """

    # Verify that the ML Model exists
    model = db.query(MLModel).filter(
        MLModel.id == model_id
    ).first()

    if not model:
        raise HTTPException(
            status_code=404,
            detail="ML Model not found."
        )
    
    existing_baseline = db.query(Dataset).filter(
        Dataset.model_id == model_id,
        Dataset.dataset_type == "BASELINE"
    ).first()

    if existing_baseline:
        raise HTTPException(
            status_code=400,
            detail="Baseline dataset already exists for this ML Model."
        )

    metadata = extract_csv_metadata(file)

    file.file.seek(0)

    file_path = save_uploaded_file(file)

    return _create_dataset_with_processing(
    db=db,
    name=name,
    owner_id=model.owner_id,
    model_id=model.id,
    dataset_type="BASELINE",
    file_path=file_path,
    metadata=metadata
)

def register_batch_dataset(
    db: Session,
    model_id: int,
    name: str,
    file: UploadFile
):
    """
    Register a new production batch for an ML Model.
    """

    # Verify ML Model exists
    model = db.query(MLModel).filter(
        MLModel.id == model_id
    ).first()

    if not model:
        raise HTTPException(
            status_code=404,
            detail="ML Model not found."
        )

    # Verify baseline dataset exists
    baseline_dataset = db.query(Dataset).filter(
        Dataset.model_id == model_id,
        Dataset.dataset_type == "BASELINE"
    ).first()

    if not baseline_dataset:
        raise HTTPException(
            status_code=400,
            detail="Baseline dataset not found for this ML Model."
        )

    # Extract metadata
    metadata = extract_csv_metadata(file)

    # Reset file pointer
    file.file.seek(0)

    # Save uploaded CSV
    file_path = save_uploaded_file(file)

    # Create batch dataset and trigger processing
    return _create_dataset_with_processing(
        db=db,
        name=name,
        owner_id=model.owner_id,
        model_id=model.id,
        dataset_type="BATCH",
        file_path=file_path,
        metadata=metadata
    )