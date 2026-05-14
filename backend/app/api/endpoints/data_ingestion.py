from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List
from app.services.data_ingestion.file_handler import handle_file_upload
from app.services.data_ingestion.url_handler import handle_url_import
from app.services.data_ingestion.validator import validate_data

router = APIRouter()

ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx", "json", "parquet"}


class UrlImportRequest(BaseModel):
    url: str


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


@router.post("/upload-file/")
async def upload_file_legacy(file: UploadFile = File(...)):
    try:
        data = await handle_file_upload(file)
        validation_errors = validate_data(data)
        if validation_errors:
            raise HTTPException(status_code=400, detail=validation_errors)
        return {"message": "File uploaded successfully", "data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import-url/")
async def import_url_legacy(url: str):
    try:
        data = await handle_url_import(url)
        validation_errors = validate_data(data)
        if validation_errors:
            raise HTTPException(status_code=400, detail=validation_errors)
        return {"message": "Data imported successfully", "data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
