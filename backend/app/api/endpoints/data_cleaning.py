from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.services.data_cleaning.imputation import perform_imputation
from app.services.data_cleaning.outlier_detection import detect_outliers
from app.services.data_cleaning.scaling import scale_data
from app.services.data_cleaning.encoding import encode_categorical

router = APIRouter()

class DataCleaningRequest(BaseModel):
    data: List[Dict]
    imputation_method: str = None
    outlier_detection: bool = False
    scaling_method: str = None
    encoding_method: str = None

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