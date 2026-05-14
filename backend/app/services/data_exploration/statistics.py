import math
import os
from scipy import stats
import pandas as pd


def _scalar(val):
    """Convert numpy scalar to a JSON-safe Python type; NaN becomes None."""
    if val is None:
        return None
    try:
        f = float(val)
        return None if math.isnan(f) or math.isinf(f) else f
    except (TypeError, ValueError):
        return val


def calculate_summary_statistics(data) -> dict:
    """Calculate summary statistics for the given DataFrame or list of dicts."""
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data
    summary = {}
    for col in df.select_dtypes(include='number').columns:
        summary[f'mean_{col}'] = _scalar(df[col].mean())
        summary[f'median_{col}'] = _scalar(df[col].median())
        summary[f'std_{col}'] = _scalar(df[col].std())
        summary[f'min_{col}'] = _scalar(df[col].min())
        summary[f'max_{col}'] = _scalar(df[col].max())
    return summary

def calculate_correlation_matrix(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate the correlation matrix for the given DataFrame."""
    correlation_matrix = data.corr()
    return correlation_matrix

def detect_outliers(data: pd.Series) -> dict:
    """Detect outliers in a given Series using Z-score method."""
    z_scores = stats.zscore(data)
    outliers = data[(z_scores > 3) | (z_scores < -3)]
    return {
        'outliers': outliers,
        'num_outliers': len(outliers)
    }

def get_variable_distribution(data: pd.Series) -> dict:
    """Get the distribution of a variable."""
    distribution = {
        'value_counts': data.value_counts(),
        'unique_values': data.unique(),
        'num_unique': data.nunique()
    }
    return distribution

def calculate_missing_data_statistics(data: pd.DataFrame) -> dict:
    """Calculate statistics related to missing data in the DataFrame."""
    missing_data_stats = {
        'total_missing': data.isnull().sum().sum(),
        'missing_percentage': (data.isnull().mean() * 100).round(2)
    }
    return missing_data_stats


def load_dataframe(file_path: str) -> pd.DataFrame:
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".csv":
        return pd.read_csv(file_path)
    elif ext in (".xls", ".xlsx"):
        return pd.read_excel(file_path)
    elif ext == ".json":
        return pd.read_json(file_path)
    elif ext == ".parquet":
        return pd.read_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def calculate_statistics(dataset_id: str) -> dict:
    df = load_dataframe(dataset_id)

    summary = calculate_summary_statistics(df)
    missing = calculate_missing_data_statistics(df)
    missing_pct = {k: _scalar(v) for k, v in missing["missing_percentage"].to_dict().items()}
    return {
        **summary,
        "total_missing": int(missing["total_missing"]),
        "missing_percentage": missing_pct,
        "row_count": len(df),
        "column_count": len(df.columns),
    }