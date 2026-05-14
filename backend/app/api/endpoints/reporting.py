import os
import uuid
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from app.services.reporting.pdf_generator import PDFGenerator
from app.services.reporting.csv_exporter import CSVExporter
from app.services.data_exploration.statistics import load_dataframe, calculate_statistics

router = APIRouter()


class ReportRequest(BaseModel):
    dataset_id: str
    title: Optional[str] = "Telehealth Hypertension Analytics Report"


@router.post("/reports/pdf")
async def create_pdf_report(request: ReportRequest):
    try:
        df = load_dataframe(request.dataset_id)
        stats = calculate_statistics(request.dataset_id)

        gen = PDFGenerator()
        gen.add_title(request.title)

        # Dataset overview
        gen.add_section("Dataset Overview",
            f"Total patients: {len(df)}  |  Columns: {', '.join(df.columns.tolist())}"
        )

        # Risk
        if "hypertension" in df.columns:
            rate = round(float(df["hypertension"].mean() * 100), 1)
            gen.add_section("Hypertension Risk",
                f"Hypertension prevalence: {rate}% of patients ({int(df['hypertension'].sum())} of {len(df)})"
            )

        # Summary statistics per numeric column
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        for col in numeric_cols:
            mean_val = stats.get(f"mean_{col}")
            std_val  = stats.get(f"std_{col}")
            min_val  = stats.get(f"min_{col}")
            max_val  = stats.get(f"max_{col}")
            if mean_val is not None:
                gen.add_section(
                    col.replace("_", " ").title(),
                    f"Mean: {mean_val}  |  Std Dev: {std_val}  |  Min: {min_val}  |  Max: {max_val}"
                )

        os.makedirs("uploads/reports", exist_ok=True)
        filename = f"uploads/reports/report_{uuid.uuid4().hex[:8]}.pdf"
        gen.save_pdf(filename)

        return FileResponse(
            path=filename,
            media_type="application/pdf",
            filename="hypertension_report.pdf",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/reports/csv")
async def create_csv_export(request: ReportRequest):
    try:
        df = load_dataframe(request.dataset_id)

        os.makedirs("uploads/exports", exist_ok=True)
        filepath = f"uploads/exports/export_{uuid.uuid4().hex[:8]}.csv"

        exporter = CSVExporter(df)
        exporter.export_to_csv(filepath)

        return FileResponse(
            path=filepath,
            media_type="text/csv",
            filename="hypertension_data.csv",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
