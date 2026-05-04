from pydantic import BaseModel, ValidationError
import pandas as pd
import json
from typing import List

class DataValidator(BaseModel):
    required_columns: list
    column_types: dict

    def validate_dataframe(self, df: pd.DataFrame) -> bool:
        if not all(col in df.columns for col in self.required_columns):
            raise ValueError(f"Missing required columns: {set(self.required_columns) - set(df.columns)}")
        
        for col, expected_type in self.column_types.items():
            if not pd.api.types.is_dtype_equal(df[col].dtype, expected_type):
                raise ValueError(f"Column '{col}' must be of type {expected_type}, but got {df[col].dtype}")
        
        return True

def validate_json(data: str) -> dict:
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON data: {e}")

def validate_csv(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise ValueError(f"Error reading CSV file: {e}")

def validate_excel(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")

def validate_data_with_schema(
    file_path: str, data_format: str, validator: DataValidator
) -> pd.DataFrame:
    """Validate data file with explicit schema validator."""
    if data_format == 'csv':
        df = validate_csv(file_path)
    elif data_format == 'excel':
        df = validate_excel(file_path)
    else:
        raise ValueError("Unsupported data format. Please use 'csv' or 'excel'.")

    validator.validate_dataframe(df)
    return df


def validate_data(data: dict) -> List[str]:
    """
    Validate uploaded data and return list of validation errors.

    Args:
        data: Dictionary containing uploaded file info with 'preview' and 'columns'

    Returns:
        List of validation error messages (empty if validation passes)
    """
    errors = []

    # Basic validation checks
    if not data:
        errors.append("No data provided")
        return errors

    if "columns" not in data or not data["columns"]:
        errors.append("No columns found in data")

    if "rows" in data and data["rows"] == 0:
        errors.append("Data file is empty")

    if "preview" in data and isinstance(data["preview"], list):
        # Check for completely empty rows
        for i, row in enumerate(data["preview"]):
            if all(v is None or v == "" for v in row.values()):
                errors.append(f"Row {i + 1} is completely empty")
                break  # Only report first empty row

    return errors