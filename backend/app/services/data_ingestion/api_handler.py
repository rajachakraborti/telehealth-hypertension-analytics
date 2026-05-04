from fastapi import APIRouter, HTTPException
from ..services.data_ingestion.file_handler import handle_file_upload
from ..services.data_ingestion.url_handler import handle_url_import
from ..services.data_ingestion.validator import validate_data

router = APIRouter()

@router.post("/upload")
async def upload_file(file: bytes):
    try:
        data = await handle_file_upload(file)
        validation_result = validate_data(data)
        if not validation_result['is_valid']:
            raise HTTPException(status_code=400, detail=validation_result['errors'])
        return {"message": "File uploaded successfully", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/import-url")
async def import_url(url: str):
    try:
        data = await handle_url_import(url)
        validation_result = validate_data(data)
        if not validation_result['is_valid']:
            raise HTTPException(status_code=400, detail=validation_result['errors'])
        return {"message": "Data imported successfully from URL", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))