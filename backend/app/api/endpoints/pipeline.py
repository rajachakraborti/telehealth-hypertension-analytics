from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.pipeline.workflow_engine import WorkflowEngine

router = APIRouter()

workflow_engine = WorkflowEngine()

PIPELINE_STAGES = [
    {"id": "ingestion",     "name": "Data Ingestion",    "description": "Upload or import a dataset (CSV, Excel, JSON)"},
    {"id": "exploration",   "name": "Data Exploration",  "description": "Inspect summary statistics, data table, and correlations"},
    {"id": "cleaning",      "name": "Data Cleaning",     "description": "Impute missing values and detect outliers"},
    {"id": "modeling",      "name": "Modeling",          "description": "Train and tune predictive models"},
    {"id": "visualization", "name": "Visualization",     "description": "Build charts and review the risk gauge"},
    {"id": "reporting",     "name": "Reporting",         "description": "Generate PDF or CSV reports"},
]


@router.post("/start")
async def start_pipeline():
    try:
        workflow_engine.start([s["name"] for s in PIPELINE_STAGES])
        return {"message": "Pipeline started.", "status": workflow_engine.get_status()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop_pipeline():
    try:
        workflow_engine.stop()
        return {"message": "Pipeline stopped.", "status": workflow_engine.get_status()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reset")
async def reset_pipeline():
    try:
        workflow_engine.reset_pipeline()
        return {"message": "Pipeline reset.", "status": workflow_engine.get_status()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advance")
async def advance_pipeline():
    """Mark the current step complete and move to the next."""
    try:
        status = workflow_engine.get_status()
        if status["status"] != "running":
            raise HTTPException(status_code=400, detail="Pipeline is not running.")
        idx = status["current_step"]
        if idx >= status["total_steps"]:
            raise HTTPException(status_code=400, detail="Pipeline already complete.")
        workflow_engine.execute_step(idx)
        new_status = workflow_engine.get_status()
        if new_status["current_step"] >= new_status["total_steps"]:
            workflow_engine.stop()
            new_status = workflow_engine.get_status()
        return {"status": new_status}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_pipeline_status():
    try:
        return {"status": workflow_engine.get_status()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/workflow")
async def get_workflow():
    return {"stages": PIPELINE_STAGES}
