from typing import List


def get_feature_severity(
    psi: float,
    ks_drift: bool,
    js: float
) -> str:
    """
    Determine overall feature severity based on
    PSI, KS Test and JS Divergence.
    """

    score = 0

    # PSI contribution
    if psi >= 0.25:
        score += 2
    elif psi >= 0.10:
        score += 1

    # KS contribution
    if ks_drift:
        score += 1

    # JS contribution
    if js >= 0.20:
        score += 2
    elif js >= 0.10:
        score += 1

    if score >= 5:
        return "Critical"

    if score >= 3:
        return "Moderate"

    if score >= 1:
        return "Minor"

    return "None"


def rank_features(
    psi_results: dict,
    ks_results: dict,
    js_results: dict
) -> List[dict]:

    ranking = []

    for feature in psi_results.keys():

        psi = psi_results[feature]["psi"]

        ks = ks_results[feature]["drift_detected"]

        js = js_results[feature]["js_divergence"]

        severity = get_feature_severity(
            psi,
            ks,
            js
        )

        ranking.append(
            {
                "feature": feature,
                "psi": psi,
                "ks_drift": ks,
                "js_divergence": js,
                "severity": severity
            }
        )

    severity_order = {
        "Critical": 4,
        "Moderate": 3,
        "Minor": 2,
        "None": 1
    }

    ranking.sort(
        key=lambda item: (
            severity_order[item["severity"]],
            item["psi"]
        ),
        reverse=True
    )

    return ranking