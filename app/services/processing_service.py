import pandas as pd
from sqlalchemy.orm import Session

from app.models.batch import Batch
from app.models.dataset import Dataset

from app.utils.profiler import (
    generate_dataset_profile,
    get_numeric_statistics,
    get_categorical_statistics
)

def process_dataset(
    db: Session,
    batch_id: int
):
    batch = db.query(Batch).filter(
        Batch.id == batch_id
    ).first()

    if not batch:
        raise ValueError("Batch not found.")

    dataset = db.query(Dataset).filter(
        Dataset.id == batch.dataset_id
    ).first()

    if not dataset:
        raise ValueError("Dataset not found.")

    try:
        batch.status = "Processing"
        db.commit()

        df = pd.read_csv(dataset.file_path)

        profile = generate_dataset_profile(df)

        profile["numeric_statistics"] = get_numeric_statistics(df)

        profile["categorical_statistics"] = get_categorical_statistics(df)

        batch.status = "Completed"
        db.commit()

        return profile

    except Exception:
        batch.status = "Failed"
        db.commit()
        raise