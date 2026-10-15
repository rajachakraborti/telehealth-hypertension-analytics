import math
import re
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.data_exploration.statistics import calculate_statistics, load_dataframe, _scalar
from app.services.data_exploration.visualization_data import prepare_visualization_data

router = APIRouter()


class DatasetRequest(BaseModel):
    dataset_id: str


def find_column(df, name: str):
    """Find a column ignoring case, spaces and underscores ('SystolicBP' matches 'systolic_bp')."""
    key = lambda c: re.sub(r"[^a-z0-9]", "", str(c).lower())
    lookup = {key(c): c for c in df.columns}
    return lookup.get(key(name))


@router.post("/statistics")
async def get_statistics(request: DatasetRequest):
    try:
        statistics = calculate_statistics(request.dataset_id)
        return {"statistics": statistics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/preview")
async def get_preview(request: DatasetRequest):
    try:
        df = load_dataframe(request.dataset_id)
        records = df.head(100).where(df.head(100).notna(), other=None).to_dict(orient="records")
        safe = [
            {k: (v if not isinstance(v, float) or not math.isnan(v) else None) for k, v in row.items()}
            for row in records
        ]
        return {"columns": list(df.columns), "rows": safe}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/correlation")
async def get_correlation(request: DatasetRequest):
    try:
        df = load_dataframe(request.dataset_id)
        numeric = df.select_dtypes(include="number")
        corr = numeric.corr()
        cols = list(corr.columns)
        records = []
        for col in cols:
            row = {"column": col}
            for other in cols:
                row[other] = _scalar(corr.loc[col, other])
            records.append(row)
        return {"columns": cols, "rows": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dashboard")
async def get_dashboard(request: DatasetRequest):
    try:
        df = load_dataframe(request.dataset_id)

        # Risk score: % of positive hypertension cases if column exists,
        # otherwise normalise mean systolic BP (120=0%, 180=100%).
        risk_score = 0.0
        htn_col, sbp_col = find_column(df, "hypertension"), find_column(df, "systolic_bp")
        if htn_col:
            risk_score = round(float(df[htn_col].mean() * 100), 1)
        elif sbp_col:
            mean_sbp = float(df[sbp_col].mean())
            risk_score = round(max(0.0, min(100.0, (mean_sbp - 120) / 60 * 100)), 1)

        stats = {}
        for name in ("age", "systolic_bp", "diastolic_bp", "bmi", "cholesterol"):
            col = find_column(df, name)
            if col:
                stats[name] = round(float(df[col].mean()), 1)

        return {
            "risk_score": risk_score,
            "total_patients": len(df),
            "stats": stats,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/visualization-data")
async def get_visualization_data(dataset_id: str):
    try:
        visualization_data = prepare_visualization_data(dataset_id)
        return {"visualization_data": visualization_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))