from sklearn.impute import SimpleImputer, KNNImputer
import pandas as pd

class DataImputer:
    def __init__(self, strategy='mean'):
        self.strategy = strategy
        self.imputer = SimpleImputer(strategy=self.strategy)

    def fit(self, data):
        """Fit the imputer on the data."""
        self.imputer.fit(data)

    def transform(self, data):
        """Transform the data by imputing missing values."""
        return self.imputer.transform(data)

    def fit_transform(self, data):
        """Fit the imputer and transform the data in one step."""
        return self.imputer.fit_transform(data)

    def set_strategy(self, strategy):
        """Set a new imputation strategy."""
        self.strategy = strategy
        self.imputer = SimpleImputer(strategy=self.strategy)

def impute_missing_values(data, strategy='mean'):
    """Impute missing values in the DataFrame using the specified strategy."""
    imputer = DataImputer(strategy)
    return imputer.fit_transform(data)


def mean_imputation(data: pd.DataFrame, column: str) -> pd.Series:
    return data[column].fillna(data[column].mean())


def median_imputation(data: pd.DataFrame, column: str) -> pd.Series:
    return data[column].fillna(data[column].median())


def perform_imputation_df(df: pd.DataFrame, method: str) -> pd.DataFrame:
    """Apply imputation to a DataFrame in-place on numeric columns."""
    df = df.copy()
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) == 0:
        return df

    if method == 'mice':
        from sklearn.experimental import enable_iterative_imputer  # noqa: F401
        from sklearn.impute import IterativeImputer
        imputer = IterativeImputer(random_state=42, max_iter=10)
    elif method == 'knn':
        imputer = KNNImputer(n_neighbors=5)
    else:
        strategy = method if method in ('mean', 'median', 'most_frequent') else 'mean'
        imputer = SimpleImputer(strategy=strategy)

    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    return df


def perform_imputation(data: list, method: str) -> list:
    """
    Perform imputation on data records.

    Args:
        data: List of dictionaries representing data records
        method: Imputation method (mean, median, most_frequent, constant)

    Returns:
        List of dictionaries with missing values imputed
    """
    df = pd.DataFrame(data)
    numeric_cols = df.select_dtypes(include=['number']).columns

    if len(numeric_cols) > 0:
        imputer = DataImputer(strategy=method)
        df[numeric_cols] = imputer.fit_transform(df[numeric_cols])

    return df.to_dict(orient='records')