from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
import pandas as pd
from typing import List, Dict


class DataScaler:
    def __init__(self, method='minmax'):
        self.method = method
        self.scaler = self._initialize_scaler()

    def _initialize_scaler(self):
        if self.method == 'minmax':
            return MinMaxScaler()
        elif self.method == 'standard':
            return StandardScaler()
        elif self.method == 'robust':
            return RobustScaler()
        else:
            raise ValueError("Invalid scaling method. Choose 'minmax', 'standard', or 'robust'.")

    def fit(self, data):
        self.scaler.fit(data)

    def transform(self, data):
        return self.scaler.transform(data)

    def fit_transform(self, data):
        return self.scaler.fit_transform(data)


def scale_data(data: List[Dict], method: str) -> List[Dict]:
    """
    Scale numeric data using the specified method.

    Args:
        data: List of dictionaries representing data records
        method: Scaling method (minmax, standard, robust)

    Returns:
        List of dictionaries with scaled numeric values
    """
    df = pd.DataFrame(data)
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

    if len(numeric_cols) > 0:
        scaler = DataScaler(method=method)
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])

    return df.to_dict(orient='records')