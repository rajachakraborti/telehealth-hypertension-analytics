from typing import List, Dict, Any
import pandas as pd
import os
import uuid

class CSVExporter:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def export_to_csv(self, file_path: str, include_index: bool = False) -> None:
        """
        Exports the DataFrame to a CSV file.

        Parameters:
        - file_path: str - The path where the CSV file will be saved.
        - include_index: bool - Whether to include the DataFrame index in the CSV file.
        """
        try:
            self.data.to_csv(file_path, index=include_index)
            print(f"Data exported successfully to {file_path}")
        except Exception as e:
            print(f"An error occurred while exporting to CSV: {e}")

    def export_multiple_to_csv(self, file_paths: List[str], include_index: bool = False) -> None:
        """
        Exports the DataFrame to multiple CSV files.

        Parameters:
        - file_paths: List[str] - A list of paths where the CSV files will be saved.
        - include_index: bool - Whether to include the DataFrame index in the CSV files.
        """
        for file_path in file_paths:
            self.export_to_csv(file_path, include_index)


def export_to_csv(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Export data to CSV file.

    Args:
        data: Dictionary containing data to export, with keys:
            - records: List of dictionaries representing data rows
            - filename: Optional filename for the export

    Returns:
        Dictionary with export status and file path
    """
    records = data.get('records', [])
    filename = data.get('filename', f"export_{uuid.uuid4().hex[:8]}.csv")

    # Create DataFrame from records
    df = pd.DataFrame(records)

    # Ensure exports directory exists
    os.makedirs('uploads/exports', exist_ok=True)
    filepath = f"uploads/exports/{filename}"

    # Export to CSV
    exporter = CSVExporter(df)
    exporter.export_to_csv(filepath)

    return {
        "status": "success",
        "filepath": filepath,
        "rows": len(df),
        "columns": list(df.columns)
    }