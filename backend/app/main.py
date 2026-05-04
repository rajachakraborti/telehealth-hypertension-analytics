from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings
import logging

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
        if not db.query(User).filter(User.username == "testuser").first():
            db.add(User(
                username="testuser",
                email="test@example.com",
                hashed_password="testpass123",
                role="clinician",
                is_active=True,
                is_superuser=False,
            ))
            db.commit()
            logger.info("Seeded default user: testuser / testpass123")
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

# Include the API router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to the Telehealth Hypertension Predictive Analytics System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)