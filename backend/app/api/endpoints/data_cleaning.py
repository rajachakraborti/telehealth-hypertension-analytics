import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.services.data_cleaning.imputation import perform_imputation, perform_imputation_df
from app.services.data_cleaning.outlier_detection import detect_outliers, detect_outliers_iqr, detect_outliers_zscore
from app.services.data_cleaning.scaling import scale_data
from app.services.data_cleaning.encoding import encode_categorical
from app.services.data_exploration.statistics import load_dataframe

router = APIRouter()


class ImputationRequest(BaseModel):
    dataset_id: str
    imputation_method: str = 'mean'


class OutlierRequest(BaseModel):
    dataset_id: str
    method: str = 'iqr'


class DataCleaningRequest(BaseModel):
    data: List[Dict]
    imputation_method: str = None
    outlier_detection: bool = False
    scaling_method: str = None
    encoding_method: str = None


@router.post("/impute")
async def impute_data(request: ImputationRequest):
    try:
        df = load_dataframe(request.dataset_id)
        missing_before = int(df.isnull().sum().sum())
        df_clean = perform_imputation_df(df, request.imputation_method)
        missing_after = int(df_clean.isnull().sum().sum())

        ext = os.path.splitext(request.dataset_id)[1].lower()
        if ext == '.csv':
            df_clean.to_csv(request.dataset_id, index=False)
        elif ext in ('.xls', '.xlsx'):
            df_clean.to_excel(request.dataset_id, index=False)

        return {
            "message": "Imputation applied successfully",
            "method": request.imputation_method,
            "missing_before": missing_before,
            "missing_after": missing_after,
            "values_imputed": missing_before - missing_after,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/detect-outliers")
async def detect_outliers_endpoint(request: OutlierRequest):
    try:
        df = load_dataframe(request.dataset_id)
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        results = []
        for col in numeric_cols:
            if request.method == 'zscore':
                outlier_series = detect_outliers_zscore(df[col].dropna())
            else:
                outlier_series = detect_outliers_iqr(df[col].dropna())
            results.append({
                "column": col,
                "outlier_count": int(len(outlier_series)),
                "total_count": int(df[col].count()),
                "outlier_values": [round(float(v), 4) for v in outlier_series.tolist()],
                "lower_bound": round(float(df[col].quantile(0.25) - 1.5 * (df[col].quantile(0.75) - df[col].quantile(0.25))), 4),
                "upper_bound": round(float(df[col].quantile(0.75) + 1.5 * (df[col].quantile(0.75) - df[col].quantile(0.25))), 4),
            })
        return {"results": results, "method": request.method}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clean")
async def clean_data(request: DataCleaningRequest):
    try:
        cleaned_data = request.data
        
        if request.imputation_method:
            cleaned_data = perform_imputation(cleaned_data, request.imputation_method)
        
        if request.outlier_detection:
            cleaned_data = detect_outliers(cleaned_data)
        
        if request.scaling_method:
            cleaned_data = scale_data(cleaned_data, request.scaling_method)
        
        if request.encoding_method:
            cleaned_data = encode_categorical(cleaned_data, request.encoding_method)
        
        return {"cleaned_data": cleaned_data}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))