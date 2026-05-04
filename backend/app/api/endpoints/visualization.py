from fastapi import APIRouter, HTTPException
from typing import List, Dict
from app.services.data_exploration.visualization_data import prepare_visualization_data

router = APIRouter()

@router.get("/visualizations/charts", response_model=List[Dict])
async def get_charts_data(dataset_id: str):
    try:
        data = prepare_visualization_data(dataset_id)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/visualizations/dashboard", response_model=Dict)
async def get_dashboard_data(dataset_id: str):
    try:
        data = prepare_visualization_data(dataset_id)
        # Additional processing for dashboard data can be added here
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/visualizations/risk-gauge", response_model=Dict)
async def get_risk_gauge_data(dataset_id: str):
    try:
        data = prepare_visualization_data(dataset_id)
        # Additional processing for risk gauge data can be added here
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))