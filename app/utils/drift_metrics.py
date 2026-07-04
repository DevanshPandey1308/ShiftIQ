import numpy as np
import pandas as pd


def calculate_psi(
    baseline_df: pd.DataFrame,
    batch_df: pd.DataFrame,
    numeric_columns: list[str]
):
    psi_results = {}

    for column in numeric_columns:

        baseline = baseline_df[column].dropna()

        batch = batch_df[column].dropna()

        baseline_hist, bin_edges = np.histogram(
            baseline,
            bins=10
        )

        batch_hist, _ = np.histogram(
            batch,
            bins=bin_edges
        )

        baseline_pct = baseline_hist / max(
            baseline_hist.sum(),
            1
        )

        batch_pct = batch_hist / max(
            batch_hist.sum(),
            1
        )

        baseline_pct = np.where(
            baseline_pct == 0,
            0.0001,
            baseline_pct
        )

        batch_pct = np.where(
            batch_pct == 0,
            0.0001,
            batch_pct
        )

        psi = np.sum(
            (baseline_pct - batch_pct)
            * np.log(
                baseline_pct / batch_pct
            )
        )

        if psi < 0.1:
            status = "No Drift"
        elif psi < 0.25:
            status = "Moderate Drift"
        else:
            status = "Significant Drift"

        psi_results[column] = {
            "psi": round(float(psi), 4),
            "status": status
        }

    return psi_results