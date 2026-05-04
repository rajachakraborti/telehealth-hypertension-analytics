from fastapi import HTTPException
import requests
import pandas as pd
from typing import Dict, Any


class URLHandler:
    @staticmethod
    def fetch_data_from_url(url: str):
        try:
            response = requests.get(url, timeout=10)
            # Accept any HTTP response — connection errors indicate an invalid URL
            try:
                return response.json()
            except Exception:
                return {"raw": response.text[:500]}
        except requests.exceptions.ConnectionError as e:
            raise requests.exceptions.RequestException(str(e))
        except requests.exceptions.RequestException as req_err:
            raise

    @staticmethod
    def validate_url(url: str) -> bool:
        # Basic URL validation logic
        if url.startswith("http://") or url.startswith("https://"):
            return True
        return False

    @staticmethod
    def ingest_data(url: str):
        if not URLHandler.validate_url(url):
            raise HTTPException(status_code=400, detail="Invalid URL format.")
        
        data = URLHandler.fetch_data_from_url(url)
        # Further processing of the data can be done here
        return data


async def handle_url_import(url: str) -> Dict[str, Any]:
    """
    Handle URL import and return data as dictionary for API response.

    Args:
        url: The URL to fetch data from

    Returns:
        Dictionary containing the fetched data
    """
    data = URLHandler.ingest_data(url)

    # If data is a list of records, convert to DataFrame for consistent handling
    if isinstance(data, list):
        df = pd.DataFrame(data)
        return {
            "url": url,
            "rows": len(df),
            "columns": list(df.columns),
            "preview": df.head(10).to_dict(orient="records"),
            "data": data
        }
    else:
        return {
            "url": url,
            "data": data
        }