import numpy as np
import pandas as pd

from scipy.stats import (
    ks_2samp,
    chi2_contingency
)

from scipy.spatial.distance import (
    jensenshannon
)


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

def calculate_ks_test(
    baseline_df: pd.DataFrame,
    batch_df: pd.DataFrame,
    numeric_columns: list[str]
):
    ks_results = {}

    for column in numeric_columns:

        statistic, p_value = ks_2samp(
            baseline_df[column].dropna(),
            batch_df[column].dropna()
        )

        ks_results[column] = {
            "ks_statistic": round(float(statistic), 4),
            "p_value": round(float(p_value), 4),
            "drift_detected": p_value < 0.05
        }

    return ks_results

def calculate_chi_square(
    baseline_df: pd.DataFrame,
    batch_df: pd.DataFrame,
    categorical_columns: list[str]
):
    chi_results = {}

    for column in categorical_columns:

        baseline_counts = baseline_df[column].value_counts()

        batch_counts = batch_df[column].value_counts()

        categories = sorted(
            set(baseline_counts.index).union(batch_counts.index)
        )

        baseline_freq = [
            baseline_counts.get(category, 0)
            for category in categories
        ]

        batch_freq = [
            batch_counts.get(category, 0)
            for category in categories
        ]

        contingency_table = np.array([
            baseline_freq,
            batch_freq
        ])

        chi2, p_value, _, _ = chi2_contingency(
            contingency_table
        )

        chi_results[column] = {
            "chi_square": round(float(chi2), 4),
            "p_value": round(float(p_value), 4),
            "drift_detected": p_value < 0.05
        }

    return chi_results

def calculate_js_divergence(
    baseline_df: pd.DataFrame,
    batch_df: pd.DataFrame,
    numeric_columns: list[str]
):
    js_results = {}

    for column in numeric_columns:

        baseline = baseline_df[column].dropna()

        batch = batch_df[column].dropna()

        baseline_hist, bin_edges = np.histogram(
            baseline,
            bins=10,
            density=True
        )

        batch_hist, _ = np.histogram(
            batch,
            bins=bin_edges,
            density=True
        )

        baseline_hist = np.where(
            baseline_hist == 0,
            0.0001,
            baseline_hist
        )

        batch_hist = np.where(
            batch_hist == 0,
            0.0001,
            batch_hist
        )

        js = jensenshannon(
            baseline_hist,
            batch_hist
        )

        js_results[column] = {
            "js_divergence": round(float(js), 4)
        }

    return js_results

def calculate_health_score(
    psi_results: dict,
    ks_results: dict,
    chi_square_results: dict,
    js_results: dict
):
    total_score = 100

    for result in psi_results.values():

        if result["status"] == "Moderate Drift":
            total_score -= 5

        elif result["status"] == "Significant Drift":
            total_score -= 10

    for result in ks_results.values():

        if result["drift_detected"]:
            total_score -= 5

    for result in chi_square_results.values():

        if result["drift_detected"]:
            total_score -= 5

    for result in js_results.values():

        if result["js_divergence"] > 0.2:
            total_score -= 5

    return max(total_score, 0)