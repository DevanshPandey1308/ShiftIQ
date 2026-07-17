from datetime import datetime

from pydantic import BaseModel


class DriftReportResponse(BaseModel):
    id: int

    batch_id: int

    psi_results: dict

    ks_results: dict

    chi_square_results: dict

    js_results: dict

    missing_value_drift: dict | None = None

    health_score: float

    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class FeatureRankingResponse(BaseModel):
    feature: str

    psi: float

    ks_drift: bool

    js_divergence: float

    severity: str