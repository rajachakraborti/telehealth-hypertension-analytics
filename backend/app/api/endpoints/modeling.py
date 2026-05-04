from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.services.modeling.model_trainer import train_model
from app.services.modeling.hyperparameter_tuner import tune_hyperparameters
from app.services.modeling.model_evaluator import evaluate_model
from app.services.modeling.explainability import explain_model

router = APIRouter()

class ModelRequest(BaseModel):
    model_config = {'protected_namespaces': ()}
    model_type: str
    features: List[str]
    target: str
    hyperparameters: Dict[str, float]

class ModelResponse(BaseModel):
    model_config = {'protected_namespaces': ()}
    model_id: str
    metrics: Dict[str, float]
    feature_importance: Dict[str, float]

@router.post("/train", response_model=ModelResponse)
async def train_model_endpoint(request: ModelRequest):
    try:
        model_id, metrics, feature_importance = train_model(
            model_type=request.model_type,
            features=request.features,
            target=request.target,
            hyperparameters=request.hyperparameters
        )
        return ModelResponse(model_id=model_id, metrics=metrics, feature_importance=feature_importance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tune", response_model=ModelResponse)
async def tune_model_endpoint(request: ModelRequest):
    try:
        model_id, metrics, feature_importance = tune_hyperparameters(
            model_type=request.model_type,
            features=request.features,
            target=request.target,
            hyperparameters=request.hyperparameters
        )
        return ModelResponse(model_id=model_id, metrics=metrics, feature_importance=feature_importance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/evaluate", response_model=ModelResponse)
async def evaluate_model_endpoint(request: ModelRequest):
    try:
        model_id, metrics, feature_importance = evaluate_model(
            model_type=request.model_type,
            features=request.features,
            target=request.target
        )
        return ModelResponse(model_id=model_id, metrics=metrics, feature_importance=feature_importance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/explain")
async def explain_model_endpoint(model_id: str):
    try:
        explanation = explain_model(model_id=model_id)
        return explanation
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))