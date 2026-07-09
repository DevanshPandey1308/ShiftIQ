def generate_ai_insight(
    health_score: int
):
    if health_score >= 90:
        return {
            "insight": "Dataset is stable with minimal drift detected.",
            "recommendation": "No immediate action is required. Continue monitoring future batches."
        }

    elif health_score >= 70:
        return {
            "insight": "Minor drift detected in the incoming dataset.",
            "recommendation": "Monitor future batches closely. Retraining is not required yet."
        }

    elif health_score >= 40:
        return {
            "insight": "Moderate drift detected across multiple features.",
            "recommendation": "Review feature distributions and consider retraining the model soon."
        }

    else:
        return {
            "insight": "Severe drift detected across multiple features.",
            "recommendation": "Retrain the model using recent production data before further deployment."
        }