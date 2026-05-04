from fastapi import APIRouter
from .endpoints import data_ingestion, data_exploration, data_cleaning, modeling, visualization, reporting, pipeline, auth

api_router = APIRouter()

# Include the various endpoints
api_router.include_router(data_ingestion.router, prefix="/data-ingestion", tags=["Data Ingestion"])
api_router.include_router(data_exploration.router, prefix="/exploration", tags=["Data Exploration"])
api_router.include_router(data_cleaning.router, prefix="/cleaning", tags=["Data Cleaning"])
api_router.include_router(modeling.router, prefix="/modeling", tags=["Modeling"])
api_router.include_router(visualization.router, prefix="/visualization", tags=["Visualization"])
api_router.include_router(reporting.router, prefix="/reporting", tags=["Reporting"])
api_router.include_router(pipeline.router, prefix="/pipeline", tags=["Pipeline"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])