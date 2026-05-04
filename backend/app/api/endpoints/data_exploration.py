from fastapi import APIRouter, HTTPException
from app.services.data_exploration.statistics import calculate_statistics
from app.services.data_exploration.visualization_data import prepare_visualization_data

router = APIRouter()

@router.post("/statistics")
async def get_statistics(dataset_id: str):
    try:
        statistics = calculate_statistics(dataset_id)
        return {"statistics": statistics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/visualization-data")
async def get_visualization_data(dataset_id: str):
    try:
        visualization_data = prepare_visualization_data(dataset_id)
        return {"visualization_data": visualization_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))