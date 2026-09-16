from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel
from typing import List
from app.services.data_ingestion.file_handler import handle_file_upload
from app.services.data_ingestion.url_handler import handle_url_import
from app.services.data_ingestion.validator import validate_data
from app.api.dependencies import RoleChecker

# Important: This assumes we have the synthetic generator from Phase 1 available!
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../scripts"))
try:
    from synthetic_telemetry_generator import SyntheticTelemetryGenerator
except ImportError:
    SyntheticTelemetryGenerator = None

router = APIRouter()

ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx", "json", "parquet"}

class UrlImportRequest(BaseModel):
    url: str

class SyntheticGenerationRequest(BaseModel):
    num_patients: int = 20
    days_per_patient: int = 7

# Notice the RoleChecker dependency! Only clinicians or admins can trigger data generation
@router.post("/generate-synthetic-telemetry", summary="Generate ABPM Data (HIPAA RBAC Secured)")
async def generate_synthetic_telemetry(
    request: SyntheticGenerationRequest,
    current_user: dict = Depends(RoleChecker(["clinician", "administrator"]))
):
    if not SyntheticTelemetryGenerator:
        raise HTTPException(status_code=500, detail="Generator script not found")
        
    try:
        generator = SyntheticTelemetryGenerator(
            num_patients=request.num_patients, 
            days_per_patient=request.days_per_patient
        )
        df_telemetry = generator.generate_telemetry()
        
        # Save to CSV so the modeling endpoint can ingest it
        output_path = os.path.join(os.path.dirname(__file__), "../../../sample_telemetry.csv")
        df_telemetry.to_csv(output_path, index=False)
        
        # Save or process (here we just return stats)
        return {
            "message": "Synthetic telemetry generated successfully",
            "triggered_by": current_user["username"],
            "total_records": len(df_telemetry),
            "sample_data": df_telemetry.head(5).to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    extension = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="File is empty")
    await file.seek(0)

    try:
        data = await handle_file_upload(file)
        validation_errors = validate_data(data)
        if validation_errors:
            raise HTTPException(status_code=400, detail=validation_errors[0])
        return {
            "message": "File uploaded successfully",
            "filename": data["filename"],
            "rows": data["rows"],
            "columns": data["columns"],
            "dataset_id": data["file_path"],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/url")
async def import_url(request: UrlImportRequest):
    try:
        data = await handle_url_import(request.url)
        return {"message": "Data imported successfully from URL"}
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to fetch data from URL")

