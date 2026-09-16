from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Dict, Any
import os

from app.api.dependencies import RoleChecker
from app.services.modeling.model_trainer import TelehealthModelTrainer
from app.services.modeling.explainability import DualLayerExplainer
from app.core.rate_limiter import limiter

router = APIRouter()

# Data path created in Phase 1
DATA_PATH = os.path.join(os.path.dirname(__file__), "../../../sample_telemetry.csv")

class PatientTelemetry(BaseModel):
    systolic: float
    diastolic: float
    map: float
    pulse_pressure: float
    is_night: int
    is_dipper: int

@router.post("/train", summary="Train XGBoost & Isolation Forest")
@limiter.limit("5/minute")
async def train_models(
    request: Request,
    current_user: dict = Depends(RoleChecker(["administrator"]))
):
    """
    Executes the training pipeline using the synthetic ABPM telemetry data.
    Only administrators can retrain models.
    """
    try:
        trainer = TelehealthModelTrainer(DATA_PATH)
        results = trainer.execute_pipeline()
        return results
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain", summary="Generate Dual-Layer SHAP Explanation")
@limiter.limit("60/minute")
async def explain_prediction(
    request: Request,
    telemetry: PatientTelemetry,
    current_user: dict = Depends(RoleChecker(["clinician", "administrator"]))
):
    """
    Simulates a clinician requesting an AI explanation for a single telemetry reading.
    """
    try:
        explainer = DualLayerExplainer()
        result = explainer.explain_prediction(telemetry.model_dump())
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))