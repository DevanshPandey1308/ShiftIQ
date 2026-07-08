import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.batch import Batch
from app.models.dataset import Dataset

from app.utils.profiler import (
    generate_dataset_profile,
    get_numeric_statistics,
    get_categorical_statistics
)

from app.utils.drift_engine import (
    prepare_dataset_comparison
)

from app.services.drift_report_service import (
    create_drift_report
)

from app.services.alert_service import (
    create_alert
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
        batch.processing_started_at = datetime.utcnow()

        db.commit()

        df = pd.read_csv(dataset.file_path)

        profile = generate_dataset_profile(df)

        profile["numeric_statistics"] = get_numeric_statistics(df)

        profile["categorical_statistics"] = get_categorical_statistics(df)

        if dataset.dataset_type == "BATCH":

            baseline_dataset = db.query(Dataset).filter(
                Dataset.model_id == dataset.model_id,
                Dataset.dataset_type == "BASELINE"
            ).first()

            if baseline_dataset:

                comparison = prepare_dataset_comparison(
                    baseline_dataset.file_path,
                    dataset.file_path
                )

                profile["drift_analysis"] = {
                    "comparison": {
                        "numeric_columns": comparison["numeric_columns"],
                        "categorical_columns": comparison["categorical_columns"]
                    },
                    "psi_results": comparison["psi_results"],
                    "ks_results": comparison["ks_results"],
                    "chi_square_results": comparison["chi_square_results"],
                    "js_results": comparison["js_results"],
                    "health_score": comparison["health_score"]
                }

                create_drift_report(
                    db=db,
                    batch_id=batch.id,
                    psi_results=comparison["psi_results"],
                    ks_results=comparison["ks_results"],
                    chi_square_results=comparison["chi_square_results"],
                    js_results=comparison["js_results"],
                    health_score=comparison["health_score"]
                )

                health_score = comparison["health_score"]

                batch.health_score = health_score

                if health_score < 40:
                    create_alert(
                        db=db,
                        batch_id=batch.id,
                        severity="HIGH",
                        message="Severe data drift detected."
                    )

                elif health_score < 70:
                    create_alert(
                        db=db,
                        batch_id=batch.id,
                        severity="MEDIUM",
                        message="Moderate data drift detected."
                    )

                elif health_score < 90:
                    create_alert(
                        db=db,
                        batch_id=batch.id,
                        severity="LOW",
                        message="Minor data drift detected."
                    )

        batch.status = "Completed"
        batch.processing_completed_at = datetime.utcnow()

        db.commit()

        return profile

    except Exception:
        batch.status = "Failed"
        db.commit()
        raise