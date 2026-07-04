import pandas as pd
from app.utils.drift_metrics import calculate_psi

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
    return dataframe.select_dtypes(
        include=["number"]
    ).columns.tolist()


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
    baseline_df = load_dataset(baseline_path)

    batch_df = load_dataset(batch_path)

    if list(baseline_df.columns) != list(batch_df.columns):
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

    return {
        "baseline": baseline_df,
        "batch": batch_df,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "psi_results": psi_results
    }