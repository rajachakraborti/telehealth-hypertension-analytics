from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
import time
import random

from app.db.database import get_db
from app.models.clinical import Patient
from app.api.dependencies import RoleChecker
from app.core.rate_limiter import limiter

router = APIRouter()

class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    ssn_last_four: str
    contact_email: str
    date_of_birth: date

@router.post("/patients", summary="Register Patient (Tests PGP Encryption Overhead)")
@limiter.limit("20/minute")
async def create_patient(
    request: Request,
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(RoleChecker(["clinician", "administrator"]))
):
    """
    Registers a new patient. 
    In a PostgreSQL production environment, this triggers `pgp_sym_encrypt` on the PHI fields.
    For local SQLite testing, we simulate the cryptographic hashing overhead (approx 10-20ms).
    """
    # Check if email already exists
    existing = db.query(Patient).filter(Patient.contact_email == patient.contact_email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Patient with this email already exists")

    # Simulate cryptographic overhead if running on local SQLite instead of Postgres
    # (PostgreSQL's pgcrypto usually adds ~12ms of latency per encrypted row)
    engine_name = db.get_bind().dialect.name
    if engine_name == "sqlite":
        time.sleep(random.uniform(0.010, 0.020)) 

    # Create new patient record
    new_patient = Patient(
        first_name=patient.first_name,
        last_name=patient.last_name,
        ssn_last_four=patient.ssn_last_four,
        contact_email=patient.contact_email,
        date_of_birth=patient.date_of_birth,
        assigned_clinician_id=current_user.get("id", 1)
    )
    
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    
    return {
        "message": "Patient securely registered", 
        "patient_id": new_patient.id,
        "encryption_status": "Active (pgp_sym_encrypt)" if engine_name == "postgresql" else "Simulated (SQLite)"
    }
