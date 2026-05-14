from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.services.modeling.model_trainer import train_model_on_dataset
from app.services.modeling.hyperparameter_tuner import tune_model_on_dataset
from app.services.modeling.model_evaluator import evaluate_model
from app.services.modeling.explainability import explain_model

router = APIRouter()

AVAILABLE_MODELS = [
    {"id": "random_forest",       "name": "Random Forest"},
    {"id": "gradient_boosting",   "name": "Gradient Boosting"},
    {"id": "logistic_regression", "name": "Logistic Regression"},
    {"id": "xgboost",             "name": "XGBoost"},
]


class ModelRequest(BaseModel):
    model_config = {'protected_namespaces': ()}
    dataset_id: str
    model_type: str
    target: str
    features: Optional[List[str]] = None
    hyperparameters: Optional[Dict[str, float]] = None


class TuningRequest(BaseModel):
    model_config = {'protected_namespaces': ()}
    dataset_id: str
    model_type: str
    target: str
    features: Optional[List[str]] = None
    param_grid: Dict[str, List]


class ModelResponse(BaseModel):
    model_config = {'protected_namespaces': ()}
    model_id: str
    metrics: Dict[str, float]
    feature_importance: Dict[str, float]


@router.get("/models")
async def get_available_models():
    return {"models": AVAILABLE_MODELS}


@router.post("/train", response_model=ModelResponse)
async def train_model_endpoint(request: ModelRequest):
    try:
        model_id, metrics, feature_importance = train_model_on_dataset(
            dataset_id=request.dataset_id,
            model_type=request.model_type,
            target=request.target,
            features=request.features,
            hyperparameters=request.hyperparameters or {},
        )
        return ModelResponse(model_id=model_id, metrics=metrics, feature_importance=feature_importance)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/tune")
async def tune_model_endpoint(request: TuningRequest):
    try:
        result = tune_model_on_dataset(
            dataset_id=request.dataset_id,
            model_type=request.model_type,
            target=request.target,
            features=request.features,
            param_grid=request.param_grid,
        )
        return result
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