import pandas as pd

from app.utils.drift_metrics import (
    calculate_psi,
    calculate_ks_test,
    calculate_chi_square,
    calculate_js_divergence,
    calculate_health_score
)


def load_dataset(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def validate_schema(
    baseline_df: pd.DataFrame,
    batch_df: pd.DataFrame
) -> bool:
    return list(baseline_df.columns) == list(batch_df.columns)


def get_numeric_columns(
    dataframe: pd.DataFrame
) -> list[str]:

    numeric_columns = dataframe.select_dtypes(
        include=["number"]
    ).columns.tolist()

    ignored_columns = {
        "id",
        "ID",
        "customerid",
        "customer_id",
        "CustomerID"
    }

    numeric_columns = [
        column
        for column in numeric_columns
        if column not in ignored_columns
    ]

    return numeric_columns


def get_categorical_columns(
    dataframe: pd.DataFrame
) -> list[str]:
    return dataframe.select_dtypes(
        exclude=["number"]
    ).columns.tolist()


def prepare_dataset_comparison(
    baseline_path: str,
    batch_path: str
):
    baseline_df = load_dataset(
        baseline_path
    )

    batch_df = load_dataset(
        batch_path
    )

    if not validate_schema(
        baseline_df,
        batch_df
    ):
        raise ValueError(
            "Baseline and Batch datasets have different schemas."
        )

    numeric_columns = get_numeric_columns(
        baseline_df
    )

    categorical_columns = get_categorical_columns(
        baseline_df
    )

    psi_results = calculate_psi(
        baseline_df,
        batch_df,
        numeric_columns
    )

    ks_results = calculate_ks_test(
        baseline_df,
        batch_df,
        numeric_columns
    )

    chi_square_results = calculate_chi_square(
        baseline_df,
        batch_df,
        categorical_columns
    )

    js_results = calculate_js_divergence(
        baseline_df,
        batch_df,
        numeric_columns
    )

    health_score = calculate_health_score(
        psi_results,
        ks_results,
        chi_square_results,
        js_results
    )

    return {
        "baseline": baseline_df,
        "batch": batch_df,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "psi_results": psi_results,
        "ks_results": ks_results,
        "chi_square_results": chi_square_results,
        "js_results": js_results,
        "health_score": health_score
    }