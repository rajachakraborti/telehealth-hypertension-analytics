from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.router import api_router
from app.core.config import settings
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _init_db():
    """Create tables and seed a default test user on first run."""
    from app.db.database import engine, Base, SessionLocal, DATABASE_URL
    from app.models.user import User
    Base.metadata.create_all(bind=engine)
    logger.info("Database: %s", DATABASE_URL)
    db = SessionLocal()
    try:
        seed_users = [
            {"username": "admin", "email": "admin@telehealth.com", "hashed_password": "admin123", "role": "administrator", "is_superuser": True},
            {"username": "clinician", "email": "clinician@telehealth.com", "hashed_password": "clinician123", "role": "clinician", "is_superuser": False},
            {"username": "analyst", "email": "analyst@telehealth.com", "hashed_password": "analyst123", "role": "data_analyst", "is_superuser": False},
            {"username": "testuser", "email": "test@example.com", "hashed_password": "testpass123", "role": "clinician", "is_superuser": False},
        ]
        for u in seed_users:
            if not db.query(User).filter(User.username == u["username"]).first():
                db.add(User(is_active=True, **u))
        db.commit()
        logger.info("Seeded default users")
    finally:
        db.close()

_init_db()

app = FastAPI(title="Telehealth Hypertension Predictive Analytics System")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve sample data files
_STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
if os.path.isdir(_STATIC_DIR):
    app.mount("/static", StaticFiles(directory=_STATIC_DIR), name="static")

# Include the API router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the Telehealth Hypertension Predictive Analytics System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)