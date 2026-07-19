from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.drift_report import DriftReport
from app.utils.feature_ranking import rank_features

def create_drift_report(
    db: Session,
    batch_id: int,
    psi_results: dict,
    ks_results: dict,
    chi_square_results: dict,
    js_results: dict,
    missing_value_drift: dict,
    health_score: float
):
    report = DriftReport(
        batch_id=batch_id,
        psi_results=psi_results,
        ks_results=ks_results,
        chi_square_results=chi_square_results,
        js_results=js_results,
        missing_value_drift=missing_value_drift,
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

def get_feature_ranking_by_batch(
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

    return rank_features(
        psi_results=report.psi_results,
        ks_results=report.ks_results,
        js_results=report.js_results
    )

def compare_drift_reports(
    db: Session,
    batch_a: int,
    batch_b: int
):
    report_a = db.query(DriftReport).filter(
        DriftReport.batch_id == batch_a
    ).first()

    report_b = db.query(DriftReport).filter(
        DriftReport.batch_id == batch_b
    ).first()

    if not report_a or not report_b:
        raise HTTPException(
            status_code=404,
            detail="One or both drift reports not found."
        )

    health_difference = round(
        report_b.health_score - report_a.health_score,
        2
    )

    if health_difference > 0:
        trend = "Improved"
    elif health_difference < 0:
        trend = "Degraded"
    else:
        trend = "No Change"

    return {
        "batch_a_id": batch_a,
        "batch_b_id": batch_b,

        "health_score_a": report_a.health_score,
        "health_score_b": report_b.health_score,
        "health_score_change": health_difference,
        "health_trend": trend,

        "psi_comparison": {
            "batch_a": report_a.psi_results,
            "batch_b": report_b.psi_results
        },

        "ks_comparison": {
            "batch_a": report_a.ks_results,
            "batch_b": report_b.ks_results
        },

        "chi_square_comparison": {
            "batch_a": report_a.chi_square_results,
            "batch_b": report_b.chi_square_results
        },

        "js_comparison": {
            "batch_a": report_a.js_results,
            "batch_b": report_b.js_results
        },

        "missing_value_comparison": {
            "batch_a": report_a.missing_value_drift,
            "batch_b": report_b.missing_value_drift
        }
    }