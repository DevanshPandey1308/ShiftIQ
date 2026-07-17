import pandas as pd


def calculate_missing_value_drift(
    baseline_df: pd.DataFrame,
    batch_df: pd.DataFrame
):
    results = {}

    common_columns = [
        column
        for column in baseline_df.columns
        if column in batch_df.columns
    ]

    for column in common_columns:

        baseline_missing_percent = (
            baseline_df[column]
            .isnull()
            .mean()
            * 100
        )

        batch_missing_percent = (
            batch_df[column]
            .isnull()
            .mean()
            * 100
        )

        difference = abs(
            batch_missing_percent -
            baseline_missing_percent
        )

        if difference < 5:
            status = "None"

        elif difference < 15:
            status = "Minor"

        elif difference < 30:
            status = "Moderate"

        else:
            status = "Critical"

        results[column] = {
            "baseline_missing_percent": round(
                baseline_missing_percent,
                2
            ),
            "batch_missing_percent": round(
                batch_missing_percent,
                2
            ),
            "difference_percent": round(
                difference,
                2
            ),
            "status": status
        }

    return results