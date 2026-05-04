from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import pandas as pd

def one_hot_encode(data: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Apply one-hot encoding to specified columns in the DataFrame.

    Parameters:
    - data: pd.DataFrame - The input DataFrame to encode.
    - columns: list - List of column names to apply one-hot encoding.

    Returns:
    - pd.DataFrame - DataFrame with one-hot encoded columns.
    """
    encoder = OneHotEncoder(sparse=False, drop='first')
    encoded_columns = encoder.fit_transform(data[columns])
    encoded_df = pd.DataFrame(encoded_columns, columns=encoder.get_feature_names_out(columns))
    return pd.concat([data.drop(columns, axis=1).reset_index(drop=True), encoded_df], axis=1)

def label_encode(data: pd.DataFrame, column: str) -> pd.Series:
    """
    Apply label encoding to a specified column in the DataFrame.

    Parameters:
    - data: pd.DataFrame - The input DataFrame to encode.
    - column: str - The column name to apply label encoding.

    Returns:
    - pd.Series - Series with label encoded values.
    """
    encoder = LabelEncoder()
    data[column] = encoder.fit_transform(data[column])
    return data[column]


def encode_categorical(data: list, method: str) -> list:
    """
    Encode categorical columns in data.

    Args:
        data: List of dictionaries representing data records
        method: Encoding method (onehot, label)

    Returns:
        List of dictionaries with encoded categorical values
    """
    df = pd.DataFrame(data)
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

    if len(categorical_cols) == 0:
        return data

    if method == 'onehot':
        df = one_hot_encode(df, categorical_cols)
    elif method == 'label':
        for col in categorical_cols:
            label_encode(df, col)
    else:
        raise ValueError(f"Unknown encoding method: {method}")

    return df.to_dict(orient='records')