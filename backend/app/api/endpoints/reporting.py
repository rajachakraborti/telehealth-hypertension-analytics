from fastapi import APIRouter, HTTPException
from typing import List
from app.services.reporting.pdf_generator import generate_pdf_report
from app.services.reporting.csv_exporter import export_to_csv

router = APIRouter()

@router.post("/reports/pdf", response_description="Generate PDF report")
async def create_pdf_report(data: dict):
    try:
        report = generate_pdf_report(data)
        return {"message": "PDF report generated successfully", "report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reports/csv", response_description="Export data to CSV")
async def create_csv_export(data: dict):
    try:
        csv_file = export_to_csv(data)
        return {"message": "Data exported to CSV successfully", "file": csv_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))