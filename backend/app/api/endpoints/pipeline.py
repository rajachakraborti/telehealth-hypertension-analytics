from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.services.pipeline.workflow_engine import WorkflowEngine

router = APIRouter()

workflow_engine = WorkflowEngine()


class PipelineStepSchema(BaseModel):
    """Pydantic schema for pipeline step input."""
    step_name: str
    step_order: int
    parameters: Optional[Dict[str, Any]] = None


@router.post("/pipeline/start")
async def start_pipeline(steps: List[PipelineStepSchema]):
    try:
        workflow_engine.start(steps)
        return {"message": "Pipeline started successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pipeline/stop")
async def stop_pipeline():
    try:
        workflow_engine.stop()
        return {"message": "Pipeline stopped successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pipeline/status")
async def get_pipeline_status():
    try:
        status = workflow_engine.get_status()
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pipeline/execute")
async def execute_pipeline_step(step: PipelineStepSchema):
    try:
        result = workflow_engine.execute_step(step)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))