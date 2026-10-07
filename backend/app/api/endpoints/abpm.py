from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from app.api.dependencies import RoleChecker
from app.core.rate_limiter import limiter
from app.services.modeling import abpm_service

router = APIRouter()


class Reading(BaseModel):
    hour: float = Field(ge=0, lt=24, description="Clock hour, e.g. 13.5 = 13:30")
    sbp: Optional[float] = Field(None, ge=20, le=300, description="Systolic mmHg; null if the cuff failed")
    dbp: Optional[float] = Field(None, ge=10, le=200, description="Diastolic mmHg; null if the cuff failed")
    hr: Optional[float] = Field(None, ge=20, le=250, description="Heart rate bpm")
    awake: Optional[bool] = Field(None, description="Diary state; derived from bed/wake hours when omitted")


class ABPMRecord(BaseModel):
    age: float = Field(ge=18, le=110)
    bmi: float = Field(ge=10, le=80)
    bed_hour: Optional[float] = Field(None, ge=0, lt=24)
    wake_hour: Optional[float] = Field(None, ge=0, lt=24)
    readings: List[Reading] = Field(min_length=24, max_length=96)


@router.post("/classify", summary="Stage a 24-hour ABPM record with explanation")
@limiter.limit("60/minute")
def classify_abpm(request: Request, record: ABPMRecord,
                  current_user: dict = Depends(RoleChecker(["clinician", "administrator"]))):
    """Classify one patient's 24-hour ambulatory record into an ACC/AHA stage (Normal, Elevated,
    Stage 1, Stage 2) and return calibrated probabilities, TreeSHAP drivers and a manual-review flag."""
    try:
        return abpm_service.classify(record.model_dump())
    except abpm_service.InvalidRecord as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Model artifact not available")


@router.get("/model-card", summary="Model card: metrics, limitations, selection decisions")
@limiter.limit("60/minute")
def get_model_card(request: Request, current_user: dict = Depends(RoleChecker(["clinician", "administrator", "data_analyst"]))):
    try:
        return abpm_service.model_card()
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Model artifact not available")
