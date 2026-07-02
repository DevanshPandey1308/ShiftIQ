import pandas as pd


def generate_dataset_profile(df: pd.DataFrame):

    profile = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "column_names": list(df.columns),
        "column_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum())
    }

    return profile

def get_numeric_statistics(df: pd.DataFrame):

    numeric_df = df.select_dtypes(include="number")

    stats = {}

    for column in numeric_df.columns:
        stats[column] = {
            "mean": float(numeric_df[column].mean()),
            "median": float(numeric_df[column].median()),
            "minimum": float(numeric_df[column].min()),
            "maximum": float(numeric_df[column].max()),
            "std_dev": float(numeric_df[column].std())
        }

    return stats

def get_categorical_statistics(df: pd.DataFrame):

    categorical_df = df.select_dtypes(include="object")

    stats = {}

    for column in categorical_df.columns:
        stats[column] = {
            "unique_values": int(categorical_df[column].nunique()),
            "most_frequent": (
                categorical_df[column].mode()[0]
                if not categorical_df[column].mode().empty
                else None
            ),
            "missing_values": int(categorical_df[column].isnull().sum())
        }

    return stats