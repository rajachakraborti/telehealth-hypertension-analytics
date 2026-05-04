from sklearn.impute import SimpleImputer
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