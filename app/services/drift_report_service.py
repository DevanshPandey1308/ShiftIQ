from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.drift_report import DriftReport


def create_drift_report(
    db: Session,
    batch_id: int,
    psi_results: dict,
    ks_results: dict,
    chi_square_results: dict,
    js_results: dict,
    health_score: float
):
    report = DriftReport(
        batch_id=batch_id,
        psi_results=psi_results,
        ks_results=ks_results,
        chi_square_results=chi_square_results,
        js_results=js_results,
        health_score=health_score
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report

def get_all_drift_reports(
    db: Session
):
    return db.query(DriftReport).all()


def get_drift_report_by_id(
    db: Session,
    report_id: int
):
    report = db.query(DriftReport).filter(
        DriftReport.id == report_id
    ).first()

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Drift Report not found."
        )

    return report


def get_drift_report_by_batch(
    db: Session,
    batch_id: int
):
    report = db.query(DriftReport).filter(
        DriftReport.batch_id == batch_id
    ).first()

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Drift Report not found."
        )

    return report