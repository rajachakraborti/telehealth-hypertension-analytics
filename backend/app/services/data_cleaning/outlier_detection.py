from scipy import stats
import pandas as pd

def detect_outliers_iqr(data: pd.Series) -> pd.Series:
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return data[(data < lower_bound) | (data > upper_bound)]

def detect_outliers_zscore(data: pd.Series, threshold: float = 3.0) -> pd.Series:
    z_scores = stats.zscore(data)
    return data[abs(z_scores) > threshold]

def handle_outliers(data: pd.Series, method: str = 'remove') -> pd.Series:
    if method == 'remove':
        return data[~data.isin(detect_outliers_iqr(data))]
    elif method == 'replace':
        median = data.median()
        return data.where(~data.isin(detect_outliers_iqr(data)), median)
    else:
        raise ValueError("Method must be 'remove' or 'replace'.")


def detect_outliers(data, column=None):
    """
    Detect outliers in data.

    When called with (DataFrame, column_name), returns a Series of outlier values for that column.
    When called with (list_of_dicts), returns the list with outlier flag columns added.
    """
    if column is not None and isinstance(data, pd.DataFrame):
        return detect_outliers_iqr(data[column])

    df = pd.DataFrame(data)
    numeric_cols = df.select_dtypes(include=['number']).columns

    for col in numeric_cols:
        outliers = detect_outliers_iqr(df[col])
        df[f'{col}_is_outlier'] = df[col].isin(outliers)

    return df.to_dict(orient='records')