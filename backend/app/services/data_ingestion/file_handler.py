from fastapi import UploadFile, File
import pandas as pd
import os
from typing import Dict, Any, List


# Default upload directory
UPLOAD_DIRECTORY = "uploads"


class FileHandler:
    def __init__(self, upload_directory: str):
        self.upload_directory = upload_directory
        os.makedirs(self.upload_directory, exist_ok=True)

    def save_file(self, file: UploadFile) -> str:
        file_location = os.path.join(self.upload_directory, file.filename)
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        return file_location

    def read_file(self, file_path: str) -> pd.DataFrame:
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == '.csv':
            return pd.read_csv(file_path)
        elif file_extension in ['.xls', '.xlsx']:
            return pd.read_excel(file_path)
        elif file_extension == '.json':
            return pd.read_json(file_path)
        elif file_extension == '.parquet':
            return pd.read_parquet(file_path)
        else:
            raise ValueError("Unsupported file type")

    def validate_schema(self, df: pd.DataFrame, expected_schema: dict) -> bool:
        for column, dtype in expected_schema.items():
            if column not in df.columns or df[column].dtype != dtype:
                return False
        return True

    def cleanup_file(self, file_path: str) -> None:
        if os.path.exists(file_path):
            os.remove(file_path)


# Module-level instance and wrapper function for endpoint compatibility
_file_handler = FileHandler(UPLOAD_DIRECTORY)


async def handle_file_upload(file: UploadFile) -> Dict[str, Any]:
    """
    Handle file upload and return data as dictionary for API response.

    Args:
        file: The uploaded file from FastAPI endpoint

    Returns:
        Dictionary containing file info and data preview
    """
    file_path = _file_handler.save_file(file)
    try:
        df = _file_handler.read_file(file_path)
        # Convert DataFrame to dict for JSON serialization
        return {
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns),
            "preview": df.head(10).to_dict(orient="records"),
            "file_path": file_path
        }
    except Exception as e:
        _file_handler.cleanup_file(file_path)
        raise e