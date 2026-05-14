import math
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.data_exploration.statistics import calculate_statistics, load_dataframe, _scalar
from app.services.data_exploration.visualization_data import prepare_visualization_data

router = APIRouter()


class DatasetRequest(BaseModel):
    dataset_id: str


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
        if "hypertension" in df.columns:
            risk_score = round(float(df["hypertension"].mean() * 100), 1)
        elif "systolic_bp" in df.columns:
            mean_sbp = float(df["systolic_bp"].mean())
            risk_score = round(max(0.0, min(100.0, (mean_sbp - 120) / 60 * 100)), 1)

        stats = {}
        for col in ("age", "systolic_bp", "diastolic_bp", "bmi", "cholesterol"):
            if col in df.columns:
                stats[col] = round(float(df[col].mean()), 1)

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