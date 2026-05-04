from typing import List, Dict, Any
import pandas as pd


def prepare_visualization_data(data) -> Any:
    """
    Prepare data for visualization.

    When given a list of dicts, returns the list directly.
    When given a dataset_id string, returns a visualization metadata dict.
    """
    if isinstance(data, list):
        return data
    dataset_id = data
    return {
        "dataset_id": dataset_id,
        "chart_data": [],
        "labels": [],
        "metadata": {}
    }


def prepare_chart_data(
    data: List[Dict[str, Any]], chart_type: str
) -> Dict[str, Any]:
    """
    Prepare data for a specific chart type.

    Args:
        data: List of data records
        chart_type: Type of chart (bar, line, scatter, pie, etc.)

    Returns:
        Dictionary with chart-ready data
    """
    df = pd.DataFrame(data)

    if chart_type == "bar":
        return _prepare_bar_chart_data(df)
    elif chart_type == "line":
        return _prepare_line_chart_data(df)
    elif chart_type == "scatter":
        return _prepare_scatter_chart_data(df)
    elif chart_type == "pie":
        return _prepare_pie_chart_data(df)
    elif chart_type == "histogram":
        return _prepare_histogram_data(df)
    else:
        return {"data": data, "chart_type": chart_type}


def _prepare_bar_chart_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Prepare data for bar chart visualization."""
    return {
        "chart_type": "bar",
        "data": df.to_dict(orient="records"),
        "columns": list(df.columns)
    }


def _prepare_line_chart_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Prepare data for line chart visualization."""
    return {
        "chart_type": "line",
        "data": df.to_dict(orient="records"),
        "columns": list(df.columns)
    }


def _prepare_scatter_chart_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Prepare data for scatter plot visualization."""
    return {
        "chart_type": "scatter",
        "data": df.to_dict(orient="records"),
        "columns": list(df.columns)
    }


def _prepare_pie_chart_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Prepare data for pie chart visualization."""
    return {
        "chart_type": "pie",
        "data": df.to_dict(orient="records"),
        "columns": list(df.columns)
    }


def _prepare_histogram_data(df: pd.DataFrame) -> Dict[str, Any]:
    """Prepare data for histogram visualization."""
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    return {
        "chart_type": "histogram",
        "data": df.to_dict(orient="records"),
        "numeric_columns": numeric_cols
    }
